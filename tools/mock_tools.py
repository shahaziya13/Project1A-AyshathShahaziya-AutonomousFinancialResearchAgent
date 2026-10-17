"""
Mock tool implementations for ARA-1.

These functions simulate the external tools used by the Autonomous
Financial Research Agent. Real APIs will replace or extend these
implementations during later development stages.
"""

from datetime import datetime, timezone
from typing import Any


def _response(
    tool_name: str,
    data: Any,
    source: str = "mock",
    confidence: float = 0.75,
) -> dict:
    """Create a standardized response returned by mock tools."""
    return {
        "success": True,
        "tool": tool_name,
        "data": data,
        "source": source,
        "confidence": confidence,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def sec_filing_search(
    company: str,
    query: str,
    filing_type: str = "10-K",
) -> dict:
    """Simulate searching an SEC filing."""
    return _response(
        "sec_filing_search",
        {
            "company": company,
            "filing_type": filing_type,
            "query": query,
            "matches": [
                f"Mock SEC evidence related to '{query}' for {company}."
            ],
        },
        source="SEC EDGAR mock",
        confidence=0.90,
    )


def web_search(query: str, max_results: int = 5) -> dict:
    """Simulate a financial web search."""
    results = [
        {
            "title": f"Mock search result {i + 1}",
            "summary": f"Mock information related to: {query}",
            "url": f"https://example.com/result-{i + 1}",
        }
        for i in range(max_results)
    ]

    return _response(
        "web_search",
        {"query": query, "results": results},
        source="Web search mock",
        confidence=0.65,
    )


def earnings_transcript(
    company: str,
    quarter: str | None = None,
    year: int | None = None,
) -> dict:
    """Simulate retrieving an earnings transcript."""
    return _response(
        "earnings_transcript",
        {
            "company": company,
            "quarter": quarter or "latest",
            "year": year,
            "highlights": [
                "Management discussed revenue performance.",
                "Management discussed future business priorities.",
                "Analysts asked questions about risks and growth.",
            ],
        },
        source="Earnings transcript mock",
        confidence=0.80,
    )


def financial_data_api(
    company: str,
    metrics: list[str] | None = None,
    period: str | None = None,
) -> dict:
    """Simulate retrieval of structured financial data."""
    requested_metrics = metrics or [
        "revenue",
        "net_income",
        "operating_margin",
    ]

    mock_values = {
        metric: {
            "value": None,
            "status": "mock_value_not_connected",
        }
        for metric in requested_metrics
    }

    return _response(
        "financial_data_api",
        {
            "company": company,
            "period": period or "latest",
            "metrics": mock_values,
        },
        source="Financial data API mock",
        confidence=0.70,
    )


def news_sentiment(company: str, days: int = 30) -> dict:
    """Simulate financial news sentiment analysis."""
    return _response(
        "news_sentiment",
        {
            "company": company,
            "days": days,
            "sentiment": "neutral",
            "score": 0.0,
            "articles_analyzed": 5,
        },
        source="News sentiment mock",
        confidence=0.60,
    )


def vector_db_search(query: str, top_k: int = 5) -> dict:
    """Simulate semantic search of long-term memory."""
    return _response(
        "vector_db_search",
        {
            "query": query,
            "top_k": top_k,
            "results": [],
            "message": "Mock vector database contains no stored evidence yet.",
        },
        source="Vector database mock",
        confidence=0.70,
    )


def vector_db_store(
    content: str,
    source: str,
    company: str | None = None,
) -> dict:
    """Simulate storing verified evidence in long-term memory."""
    return _response(
        "vector_db_store",
        {
            "stored": True,
            "content": content,
            "original_source": source,
            "company": company,
        },
        source="Vector database mock",
        confidence=0.95,
    )


def company_profile(company: str) -> dict:
    """Simulate retrieval of a company profile."""
    return _response(
        "company_profile",
        {
            "company": company,
            "business_overview": (
                f"Mock business overview for {company}."
            ),
            "industry": "Mock industry",
            "headquarters": "Mock headquarters",
            "executives": [],
        },
        source="Company profile mock",
        confidence=0.70,
    )


def peer_comparison(
    companies: list[str],
    metrics: list[str] | None = None,
) -> dict:
    """Simulate comparison of multiple companies."""
    return _response(
        "peer_comparison",
        {
            "companies": companies,
            "metrics": metrics or ["revenue", "growth", "margin"],
            "comparison": {
                company: "Mock comparison data"
                for company in companies
            },
        },
        source="Peer comparison mock",
        confidence=0.70,
    )


def report_generator(
    title: str,
    findings: list[str],
    include_sources: bool = True,
) -> dict:
    """Simulate generation of a financial research report."""
    report_lines = [f"# {title}", ""]

    for index, finding in enumerate(findings, start=1):
        report_lines.append(f"{index}. {finding}")

    if include_sources:
        report_lines.extend(
            [
                "",
                "## Sources",
                "Mock sources will be replaced by verified sources.",
            ]
        )

    return _response(
        "report_generator",
        {
            "title": title,
            "report": "\n".join(report_lines),
        },
        source="ARA-1 report generator mock",
        confidence=0.80,
    )


def fact_checker(claim: str, evidence: list[str]) -> dict:
    """Simulate cross-checking a claim against evidence."""
    if not evidence:
        status = "unverified"
        confidence = 0.20
    else:
        status = "requires_real_source_verification"
        confidence = 0.50

    return _response(
        "fact_checker",
        {
            "claim": claim,
            "evidence_count": len(evidence),
            "status": status,
        },
        source="Fact checker mock",
        confidence=confidence,
    )


def calculation_engine(
    operation: str,
    values: list[float],
) -> dict:
    """Perform deterministic mathematical calculations."""
    if len(values) < 2:
        raise ValueError("At least two values are required.")

    if operation == "add":
        result = sum(values)

    elif operation == "subtract":
        result = values[0]
        for value in values[1:]:
            result -= value

    elif operation == "multiply":
        result = 1.0
        for value in values:
            result *= value

    elif operation == "divide":
        result = values[0]
        for value in values[1:]:
            if value == 0:
                raise ValueError("Division by zero is not allowed.")
            result /= value

    elif operation == "percentage_change":
        old_value = values[0]
        new_value = values[1]

        if old_value == 0:
            raise ValueError(
                "Old value cannot be zero for percentage change."
            )

        result = ((new_value - old_value) / abs(old_value)) * 100

    else:
        raise ValueError(f"Unsupported operation: {operation}")

    return _response(
        "calculation_engine",
        {
            "operation": operation,
            "values": values,
            "result": result,
        },
        source="ARA-1 calculation engine",
        confidence=1.0,
    )


MOCK_TOOL_FUNCTIONS = {
    "sec_filing_search": sec_filing_search,
    "web_search": web_search,
    "earnings_transcript": earnings_transcript,
    "financial_data_api": financial_data_api,
    "news_sentiment": news_sentiment,
    "vector_db_search": vector_db_search,
    "vector_db_store": vector_db_store,
    "company_profile": company_profile,
    "peer_comparison": peer_comparison,
    "report_generator": report_generator,
    "fact_checker": fact_checker,
    "calculation_engine": calculation_engine,
}