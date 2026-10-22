"""Challenge 8: NVIDIA full research stress test."""

from __future__ import annotations

import json
from pathlib import Path

from tools.tool_registry import ToolRegistry
from evaluation.failure_simulator import FailureSimulator


def main():
    registry = ToolRegistry()

    financial_simulator = FailureSimulator(
        failure_rate=0.50,
        seed=42,
    )

    sec_simulator = FailureSimulator(
        failure_rate=0.50,
        seed=42,
    )

    evidence = {}
    data_gaps = []

    # Multiple calls are intentional: Challenge 8 tests behavior
    # under a configured 50% API failure probability.
    financial_runs = []

    for _ in range(6):
        result = financial_simulator.execute(
            "financial_data_api",
            lambda **kwargs: registry.execute(
                "financial_data_api",
                kwargs,
            ),
            company="NVIDIA",
        )
        financial_runs.append(result)

    sec_runs = []

    for _ in range(6):
        result = sec_simulator.execute(
            "sec_filing_search",
            lambda **kwargs: registry.execute(
                "sec_filing_search",
                kwargs,
            ),
            company="NVIDIA",
            filing_type="10-K",
            limit=3,
        )
        sec_runs.append(result)

    evidence["financial_failure_test"] = financial_runs
    evidence["sec_failure_test"] = sec_runs

    # Other tools remain available as fallback/supplementary evidence.
    tool_calls = {
        "company_profile": {
            "company": "NVIDIA",
        },
        "web_search": {
            "query": (
                "NVIDIA latest financial performance AI data center "
                "growth risks competition"
            ),
            "max_results": 5,
        },
        "news_sentiment": {
            "company": "NVIDIA",
            "max_results": 5,
        },
        "earnings_transcript": {
            "company": "NVIDIA",
            "quarter": "latest",
            "max_results": 5,
        },
    }

    for tool_name, arguments in tool_calls.items():
        try:
            result = registry.execute(
                tool_name,
                arguments,
            )

            evidence[tool_name] = result

            if not result.get("success"):
                data_gaps.append(
                    f"{tool_name} did not return usable evidence."
                )

        except Exception as exc:
            evidence[tool_name] = {
                "success": False,
                "error": str(exc),
            }

            data_gaps.append(
                f"{tool_name} failed: {exc}"
            )

    if not any(item["success"] for item in financial_runs):
        data_gaps.append(
            "Financial API produced no successful result during "
            "the simulated-failure run."
        )

    if not any(item["success"] for item in sec_runs):
        data_gaps.append(
            "SEC filing search produced no successful result during "
            "the simulated-failure run."
        )

    output = {
        "challenge": 8,
        "company": "NVIDIA",
        "failure_configuration": {
            "financial_data_api": 0.50,
            "sec_filing_search": 0.50,
        },
        "financial_failure_statistics":
            financial_simulator.statistics(),
        "sec_failure_statistics":
            sec_simulator.statistics(),
        "data_gaps": data_gaps,
        "evidence": evidence,
    }

    Path("results").mkdir(exist_ok=True)

    Path(
        "results/challenge_8_stress_test.json"
    ).write_text(
        json.dumps(output, indent=2, default=str),
        encoding="utf-8",
    )

    print("Challenge 8 stress test complete.")
    print(
        "Financial API:",
        output["financial_failure_statistics"],
    )
    print(
        "SEC EDGAR:",
        output["sec_failure_statistics"],
    )
    print("Data gaps:", len(data_gaps))


if __name__ == "__main__":
    main()
