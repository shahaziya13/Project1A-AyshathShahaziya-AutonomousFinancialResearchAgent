"""Challenge 5: Palantir contradictory evidence analysis."""

from __future__ import annotations

import json
from pathlib import Path

from tools.tool_registry import ToolRegistry


def safe_execute(registry, tool_name, arguments):
    try:
        return registry.execute(tool_name, arguments)
    except Exception as exc:
        return {
            "success": False,
            "tool": tool_name,
            "error": str(exc),
        }


def main():
    registry = ToolRegistry()

    evidence = {}

    evidence["company_profile"] = safe_execute(
        registry,
        "company_profile",
        {"company": "Palantir"},
    )

    evidence["financial_data_api"] = safe_execute(
        registry,
        "financial_data_api",
        {"company": "Palantir"},
    )

    evidence["sec_filing_search"] = safe_execute(
        registry,
        "sec_filing_search",
        {
            "company": "Palantir",
            "filing_type": "10-K",
            "limit": 3,
        },
    )

    evidence["web_search"] = safe_execute(
        registry,
        "web_search",
        {
            "query": (
                "Palantir latest financial performance growth "
                "concerns valuation risks"
            ),
            "max_results": 5,
        },
    )

    evidence["news_sentiment"] = safe_execute(
        registry,
        "news_sentiment",
        {
            "company": "Palantir",
            "max_results": 5,
        },
    )

    evidence["earnings_transcript"] = safe_execute(
        registry,
        "earnings_transcript",
        {
            "company": "Palantir",
            "quarter": "latest",
            "max_results": 5,
        },
    )

    financial = evidence["financial_data_api"]

    fact_evidence = []

    if financial.get("success"):
        data = financial.get("data", {})

        revenue_growth = data.get("revenue_growth")

        if revenue_growth is not None:
            fact_evidence.append(
                {
                    "source": "financial_data_api",
                    "value": float(revenue_growth) * 100,
                    "supports_claim": float(revenue_growth) > 0,
                }
            )

    fact_evidence.append(
        {
            "source": "news_and_web_context",
            "supports_claim": False,
        }
    )

    evidence["fact_checker"] = safe_execute(
        registry,
        "fact_checker",
        {
            "claim": (
                "Palantir is financially struggling and "
                "not showing revenue growth."
            ),
            "evidence": fact_evidence,
            "tolerance_percent": 5,
        },
    )

    successful_tools = sum(
        1
        for result in evidence.values()
        if isinstance(result, dict)
        and result.get("success")
    )

    output = {
        "challenge": 5,
        "company": "Palantir Technologies",
        "research_question": (
            "How should contradictory negative narrative and "
            "strong financial growth evidence be reconciled?"
        ),
        "successful_tools": successful_tools,
        "evidence": evidence,
        "analysis_rule": (
            "Negative commentary must not override stronger "
            "quantitative evidence without supporting facts. "
            "Conflicting evidence must be disclosed."
        ),
    }

    Path("results").mkdir(exist_ok=True)

    Path("results/challenge_5_evidence.json").write_text(
        json.dumps(output, indent=2, default=str),
        encoding="utf-8",
    )

    print("Challenge 5 evidence collection complete.")
    print("Successful tool results:", successful_tools)
    print(
        "Financial data success:",
        evidence["financial_data_api"].get("success"),
    )
    print(
        "SEC success:",
        evidence["sec_filing_search"].get("success"),
    )
    print(
        "Fact checker:",
        evidence["fact_checker"],
    )


if __name__ == "__main__":
    main()
