from __future__ import annotations

from typing import Any

import httpx

from config.settings import settings
from tools.api_utils import (
    RateLimiter,
    TTLCache,
    cached_api_call,
)


_cache = TTLCache(ttl_seconds=900)
_rate_limiter = RateLimiter(requests_per_second=1.0)

TAVILY_SEARCH_URL = "https://api.tavily.com/search"


def _search_transcript(
    company: str,
    quarter: str,
    max_results: int,
) -> dict[str, Any]:
    """Search the web for public earnings-call transcript sources."""

    if not settings.tavily_api_key:
        raise ValueError(
            "TAVILY_API_KEY is not configured."
        )

    query = (
        f"{company} {quarter} earnings call transcript "
        f"investor relations"
    )

    payload = {
        "api_key": settings.tavily_api_key,
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False,
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(
            TAVILY_SEARCH_URL,
            json=payload,
        )
        response.raise_for_status()
        return response.json()


def earnings_transcript(
    company: str,
    quarter: str = "latest",
    max_results: int = 5,
) -> dict[str, Any]:
    """
    Discover public earnings-call transcript sources.

    The returned content consists of search excerpts and source
    references. It must not be treated as a complete verbatim
    earnings transcript.
    """

    if not company or not company.strip():
        raise ValueError("company cannot be empty.")

    if not quarter or not quarter.strip():
        raise ValueError("quarter cannot be empty.")

    if not 1 <= max_results <= 10:
        raise ValueError(
            "max_results must be between 1 and 10."
        )

    parameters = {
        "company": company.strip(),
        "quarter": quarter.strip(),
        "max_results": max_results,
    }

    try:
        response, from_cache = cached_api_call(
            namespace="earnings_transcript",
            parameters=parameters,
            cache=_cache,
            rate_limiter=_rate_limiter,
            request_function=lambda: _search_transcript(
                company=company.strip(),
                quarter=quarter.strip(),
                max_results=max_results,
            ),
        )

        results = []

        for item in response.get("results", []):
            results.append(
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "excerpt": item.get("content", ""),
                    "score": item.get("score"),
                }
            )

        return {
            "success": True,
            "tool": "earnings_transcript",
            "data": {
                "company": company.strip(),
                "quarter": quarter.strip(),
                "results": results,
                "result_count": len(results),
                "retrieval_type": (
                    "public transcript source discovery"
                ),
                "complete_transcript": False,
                "note": (
                    "Results contain public search excerpts and "
                    "source references, not a complete verbatim "
                    "earnings-call transcript."
                ),
            },
            "source": "Tavily Search API",
            "cached": from_cache,
            "confidence": 0.80,
        }

    except Exception as error:
        return {
            "success": False,
            "tool": "earnings_transcript",
            "error": str(error),
            "error_type": type(error).__name__,
        }