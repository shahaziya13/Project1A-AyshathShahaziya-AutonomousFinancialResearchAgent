"""Real financial market data integration using yfinance."""

from typing import Any

import yfinance as yf

from tools.api_utils import RateLimiter, TTLCache, cached_api_call


financial_cache = TTLCache(ttl_seconds=300)

financial_rate_limiter = RateLimiter(
    requests_per_second=2
)


COMPANY_TICKERS = {
    "microsoft": "MSFT",
    "apple": "AAPL",
    "tesla": "TSLA",
    "nvidia": "NVDA",
    "amazon": "AMZN",
    "alphabet": "GOOGL",
    "google": "GOOGL",
    "meta": "META",
    "palantir": "PLTR",
}


def resolve_ticker(company: str) -> str:
    """Convert a company name or ticker into a ticker symbol."""

    if not company or not company.strip():
        raise ValueError("company cannot be empty.")

    value = company.strip()

    lower_value = value.lower()

    if lower_value in COMPANY_TICKERS:
        return COMPANY_TICKERS[lower_value]

    # Assume short uppercase values are already ticker symbols.
    if value.isalpha() and len(value) <= 6:
        return value.upper()

    raise ValueError(
        f"Could not resolve ticker for company: {company}"
    )


def _safe_number(value: Any) -> int | float | None:
    """Convert a financial value into a JSON-safe number."""

    if value is None:
        return None

    try:
        if value != value:
            return None
    except Exception:
        pass

    if isinstance(value, (int, float)):
        return value

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _fetch_financial_data(ticker: str) -> dict[str, Any]:
    """Fetch current financial information from Yahoo Finance."""

    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "ticker": ticker,
        "company_name": info.get("longName"),
        "currency": info.get("currency"),
        "current_price": _safe_number(
            info.get("currentPrice")
        ),
        "market_cap": _safe_number(
            info.get("marketCap")
        ),
        "total_revenue": _safe_number(
            info.get("totalRevenue")
        ),
        "net_income": _safe_number(
            info.get("netIncomeToCommon")
        ),
        "trailing_eps": _safe_number(
            info.get("trailingEps")
        ),
        "forward_eps": _safe_number(
            info.get("forwardEps")
        ),
        "trailing_pe": _safe_number(
            info.get("trailingPE")
        ),
        "forward_pe": _safe_number(
            info.get("forwardPE")
        ),
        "profit_margin": _safe_number(
            info.get("profitMargins")
        ),
        "revenue_growth": _safe_number(
            info.get("revenueGrowth")
        ),
        "fifty_two_week_high": _safe_number(
            info.get("fiftyTwoWeekHigh")
        ),
        "fifty_two_week_low": _safe_number(
            info.get("fiftyTwoWeekLow")
        ),
        "website": info.get("website"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
    }


def financial_data_api(
    company: str,
    metrics: list[str] | None = None,
    period: str = "latest",
) -> dict[str, Any]:
    """Retrieve real financial data for a public company."""

    ticker = resolve_ticker(company)

    data, from_cache = cached_api_call(
        namespace="financial_data",
        parameters={
            "ticker": ticker,
            "period": period,
        },
        cache=financial_cache,
        rate_limiter=financial_rate_limiter,
        request_function=lambda: _fetch_financial_data(
            ticker
        ),
    )

    if metrics:
        filtered_data = {
            "ticker": data.get("ticker"),
            "company_name": data.get("company_name"),
        }

        for metric in metrics:
            if metric in data:
                filtered_data[metric] = data[metric]

        data = filtered_data

    return {
        "success": True,
        "tool": "financial_data_api",
        "data": data,
        "source": "Yahoo Finance via yfinance",
        "cached": from_cache,
        "confidence": 0.9,
    }

def company_profile(
    company: str,
) -> dict[str, Any]:
    """Retrieve a real company profile using yfinance."""

    ticker = resolve_ticker(company)

    def fetch_profile() -> dict[str, Any]:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "ticker": ticker,
            "company_name": info.get("longName"),
            "short_name": info.get("shortName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "city": info.get("city"),
            "website": info.get("website"),
            "employees": info.get(
                "fullTimeEmployees"
            ),
            "business_summary": info.get(
                "longBusinessSummary"
            ),
            "exchange": info.get("exchange"),
            "currency": info.get("currency"),
        }

    data, from_cache = cached_api_call(
        namespace="company_profile",
        parameters={
            "ticker": ticker,
        },
        cache=financial_cache,
        rate_limiter=financial_rate_limiter,
        request_function=fetch_profile,
    )

    return {
        "success": True,
        "tool": "company_profile",
        "data": data,
        "source": "Yahoo Finance via yfinance",
        "cached": from_cache,
        "confidence": 0.9,
    }