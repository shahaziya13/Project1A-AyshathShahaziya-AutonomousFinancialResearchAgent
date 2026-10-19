"""SEC EDGAR integration for retrieving public company filings."""

from typing import Any

import httpx

from config.settings import settings
from tools.api_utils import RateLimiter, TTLCache, cached_api_call


SEC_SUBMISSIONS_URL = (
    "https://data.sec.gov/submissions/CIK{cik}.json"
)

SEC_TICKER_URL = (
    "https://www.sec.gov/files/company_tickers.json"
)

sec_cache = TTLCache(ttl_seconds=900)

# Stay comfortably below the SEC maximum request rate.
sec_rate_limiter = RateLimiter(requests_per_second=5)


def _headers() -> dict[str, str]:
    """Return headers required for responsible SEC access."""

    return {
        "User-Agent": settings.sec_user_agent,
        "Accept-Encoding": "gzip, deflate",
        "Accept": "application/json",
    }


def _request_json(url: str) -> Any:
    """Perform an HTTP GET request and return JSON."""

    with httpx.Client(
        timeout=20.0,
        follow_redirects=True,
    ) as client:
        response = client.get(
            url,
            headers=_headers(),
        )

        response.raise_for_status()

        return response.json()


def get_company_cik(company: str) -> str:
    """Resolve a ticker or company name to its 10-digit SEC CIK."""

    if not company or not company.strip():
        raise ValueError("company cannot be empty.")

    search_value = company.strip().lower()

    data, _ = cached_api_call(
        namespace="sec_company_tickers",
        parameters={"resource": "company_tickers"},
        cache=sec_cache,
        rate_limiter=sec_rate_limiter,
        request_function=lambda: _request_json(
            SEC_TICKER_URL
        ),
    )

    exact_matches = []
    partial_matches = []

    for item in data.values():
        ticker = str(
            item.get("ticker", "")
        ).strip().lower()

        title = str(
            item.get("title", "")
        ).strip().lower()

        if search_value == ticker or search_value == title:
            exact_matches.append(item)

        elif search_value in title:
            partial_matches.append(item)

    matches = exact_matches or partial_matches

    if not matches:
        raise ValueError(
            f"Could not find SEC CIK for company: {company}"
        )

    cik = str(matches[0]["cik_str"])

    return cik.zfill(10)


def sec_filing_search(
    company: str,
    filing_type: str = "10-K",
    limit: int = 5,
) -> dict[str, Any]:
    """Retrieve recent SEC filings for a company."""

    if limit < 1 or limit > 20:
        raise ValueError(
            "limit must be between 1 and 20."
        )

    cik = get_company_cik(company)

    url = SEC_SUBMISSIONS_URL.format(
        cik=cik
    )

    data, from_cache = cached_api_call(
        namespace="sec_submissions",
        parameters={"cik": cik},
        cache=sec_cache,
        rate_limiter=sec_rate_limiter,
        request_function=lambda: _request_json(url),
    )

    recent = (
        data.get("filings", {})
        .get("recent", {})
    )

    forms = recent.get("form", [])
    accession_numbers = recent.get(
        "accessionNumber",
        [],
    )
    filing_dates = recent.get(
        "filingDate",
        [],
    )
    report_dates = recent.get(
        "reportDate",
        [],
    )
    primary_documents = recent.get(
        "primaryDocument",
        [],
    )

    filings = []

    for index, form in enumerate(forms):
        if form.upper() != filing_type.upper():
            continue

        accession = accession_numbers[index]
        accession_no_dashes = accession.replace(
            "-",
            "",
        )

        cik_without_leading_zeros = str(
            int(cik)
        )

        primary_document = primary_documents[index]

        filing_url = (
            "https://www.sec.gov/Archives/edgar/data/"
            f"{cik_without_leading_zeros}/"
            f"{accession_no_dashes}/"
            f"{primary_document}"
        )

        filings.append(
            {
                "form": form,
                "filing_date": filing_dates[index],
                "report_date": report_dates[index],
                "accession_number": accession,
                "primary_document": primary_document,
                "filing_url": filing_url,
            }
        )

        if len(filings) >= limit:
            break

    return {
        "success": True,
        "tool": "sec_filing_search",
        "data": {
            "company": data.get(
                "name",
                company,
            ),
            "cik": cik,
            "filing_type": filing_type,
            "filings": filings,
        },
        "source": "SEC EDGAR",
        "source_url": url,
        "cached": from_cache,
        "confidence": 1.0,
    }