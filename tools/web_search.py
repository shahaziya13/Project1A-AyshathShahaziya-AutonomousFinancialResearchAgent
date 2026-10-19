"""Real web search integration using the Tavily Search API."""

from typing import Any

import httpx

from config.settings import settings
from tools.api_utils import RateLimiter, TTLCache, cached_api_call


TAVILY_SEARCH_URL = "https://api.tavily.com/search"

web_search_cache = TTLCache(ttl_seconds=300)

web_search_rate_limiter = RateLimiter(
    requests_per_second=1
)


def _perform_tavily_search(
    query: str,
    max_results: int,
) -> dict[str, Any]:
    """Send a search request to Tavily."""

    if not settings.tavily_api_key:
        raise ValueError(
            "TAVILY_API_KEY is not configured."
        )

    payload = {
        "api_key": settings.tavily_api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False,
    }

    with httpx.Client(
        timeout=30.0,
        follow_redirects=True,
    ) as client:
        response = client.post(
            TAVILY_SEARCH_URL,
            json=payload,
        )

        response.raise_for_status()

        return response.json()


def web_search(
    query: str,
    max_results: int = 5,
) -> dict[str, Any]:
    """Search the web for financial research evidence."""

    if not isinstance(query, str) or not query.strip():
        raise ValueError(
            "query must be a non-empty string."
        )

    if max_results < 1 or max_results > 10:
        raise ValueError(
            "max_results must be between 1 and 10."
        )

    data, from_cache = cached_api_call(
        namespace="tavily_web_search",
        parameters={
            "query": query.strip(),
            "max_results": max_results,
        },
        cache=web_search_cache,
        rate_limiter=web_search_rate_limiter,
        request_function=lambda: _perform_tavily_search(
            query=query.strip(),
            max_results=max_results,
        ),
    )

    results = []

    for item in data.get("results", []):
        results.append(
            {
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content"),
                "score": item.get("score"),
            }
        )

    return {
        "success": True,
        "tool": "web_search",
        "data": {
            "query": query,
            "results": results,
        },
        "source": "Tavily Search API",
        "cached": from_cache,
        "confidence": 0.85,
    }