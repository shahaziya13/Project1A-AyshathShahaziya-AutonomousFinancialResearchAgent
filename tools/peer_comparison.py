from __future__ import annotations

from typing import Any

from tools.financial_api import financial_data_api


DEFAULT_METRICS = [
    "market_cap",
    "total_revenue",
    "net_income",
    "trailing_eps",
    "trailing_pe",
    "profit_margin",
    "revenue_growth",
]


def peer_comparison(
    companies: list[str],
    metrics: list[str] | None = None,
) -> dict[str, Any]:
    """
    Compare financial metrics across multiple companies.

    Financial information is retrieved through the existing
    financial_data_api tool.
    """

    if not companies:
        raise ValueError(
            "At least one company must be provided."
        )

    if len(companies) < 2:
        raise ValueError(
            "At least two companies are required for comparison."
        )

    if len(companies) > 10:
        raise ValueError(
            "A maximum of 10 companies can be compared."
        )

    selected_metrics = metrics or DEFAULT_METRICS

    comparison: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []

    for company in companies:
        result = financial_data_api(
            company=company,
            metrics=selected_metrics,
            period="latest",
        )

        if result.get("success"):
            comparison.append(
                result["data"]
            )
        else:
            failures.append(
                {
                    "company": company,
                    "error": result.get(
                        "error",
                        "Unknown error",
                    ),
                }
            )

    if not comparison:
        return {
            "success": False,
            "tool": "peer_comparison",
            "error": (
                "Financial data could not be retrieved "
                "for any requested company."
            ),
            "failures": failures,
        }

    metric_leaders: dict[str, dict[str, Any]] = {}

    for metric in selected_metrics:
        valid_values = []

        for company_data in comparison:
            value = company_data.get(metric)

            if isinstance(value, (int, float)):
                valid_values.append(
                    (
                        company_data.get(
                            "company_name",
                            company_data.get("ticker"),
                        ),
                        value,
                    )
                )

        if valid_values:
            leader = max(
                valid_values,
                key=lambda item: item[1],
            )

            metric_leaders[metric] = {
                "company": leader[0],
                "value": leader[1],
            }

    return {
        "success": True,
        "tool": "peer_comparison",
        "data": {
            "companies_requested": companies,
            "metrics": selected_metrics,
            "comparison": comparison,
            "metric_leaders": metric_leaders,
            "failures": failures,
        },
        "source": "Yahoo Finance via financial_data_api",
        "confidence": 0.85,
    }