"""News sentiment analysis using Tavily search and VADER."""

from typing import Any

import httpx
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from config.settings import settings
from tools.api_utils import RateLimiter, TTLCache, cached_api_call


TAVILY_SEARCH_URL = "https://api.tavily.com/search"

news_cache = TTLCache(ttl_seconds=300)

news_rate_limiter = RateLimiter(
    requests_per_second=1
)

sentiment_analyzer = SentimentIntensityAnalyzer()


def _search_news(
    company: str,
    max_results: int,
) -> dict[str, Any]:
    """Retrieve recent company news using Tavily."""

    if not settings.tavily_api_key:
        raise ValueError(
            "TAVILY_API_KEY is not configured."
        )

    payload = {
        "api_key": settings.tavily_api_key,
        "query": f"{company} company financial news",
        "topic": "news",
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


def _sentiment_label(compound: float) -> str:
    """Convert a VADER compound score into a label."""

    if compound >= 0.05:
        return "positive"

    if compound <= -0.05:
        return "negative"

    return "neutral"


def news_sentiment(
    company: str,
    max_results: int = 5,
) -> dict[str, Any]:
    """Retrieve company news and calculate sentiment."""

    if not isinstance(company, str) or not company.strip():
        raise ValueError(
            "company must be a non-empty string."
        )

    if max_results < 1 or max_results > 10:
        raise ValueError(
            "max_results must be between 1 and 10."
        )

    data, from_cache = cached_api_call(
        namespace="news_sentiment",
        parameters={
            "company": company.strip(),
            "max_results": max_results,
        },
        cache=news_cache,
        rate_limiter=news_rate_limiter,
        request_function=lambda: _search_news(
            company=company.strip(),
            max_results=max_results,
        ),
    )

    articles = []
    compound_scores = []

    for item in data.get("results", []):
        title = item.get("title") or ""
        content = item.get("content") or ""

        text = f"{title}. {content}".strip()

        scores = sentiment_analyzer.polarity_scores(
            text
        )

        compound = scores["compound"]

        compound_scores.append(compound)

        articles.append(
            {
                "title": title,
                "url": item.get("url"),
                "published_date": item.get(
                    "published_date"
                ),
                "content": content,
                "sentiment": {
                    "negative": scores["neg"],
                    "neutral": scores["neu"],
                    "positive": scores["pos"],
                    "compound": compound,
                    "label": _sentiment_label(
                        compound
                    ),
                },
            }
        )

    if compound_scores:
        average_compound = (
            sum(compound_scores)
            / len(compound_scores)
        )
    else:
        average_compound = 0.0

    overall_sentiment = _sentiment_label(
        average_compound
    )

    return {
        "success": True,
        "tool": "news_sentiment",
        "data": {
            "company": company,
            "article_count": len(articles),
            "overall_sentiment": overall_sentiment,
            "average_compound": round(
                average_compound,
                4,
            ),
            "articles": articles,
        },
        "source": "Tavily News Search + VADER",
        "cached": from_cache,
        "confidence": 0.8,
    }