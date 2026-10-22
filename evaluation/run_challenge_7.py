"""Challenge 7: Memory-based sector analysis."""

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

    research_query = (
        "Based on companies already researched, what trends can "
        "be identified across large technology and AI companies?"
    )

    # Memory MUST be the primary retrieval source for Challenge 7.
    memory = safe_execute(
        registry,
        "vector_db_search",
        {
            "query": (
                "Microsoft Apple Tesla Amazon Alphabet NVIDIA "
                "technology AI cloud growth risks"
            ),
            "n_results": 10,
        },
    )

    # Supplement memory rather than replacing it.
    web = safe_execute(
        registry,
        "web_search",
        {
            "query": (
                "latest technology sector AI cloud infrastructure "
                "growth risks major companies"
            ),
            "max_results": 5,
        },
    )

    output = {
        "challenge": 7,
        "research_query": research_query,
        "retrieval_strategy": {
            "primary": "vector_db_search",
            "supplementary": "web_search",
        },
        "memory_success": memory.get("success", False),
        "web_success": web.get("success", False),
        "memory_evidence": memory,
        "supplementary_web_evidence": web,
        "limitations": [
            (
                "Memory analysis is limited to research previously "
                "stored in the vector database."
            ),
            (
                "Not every earlier challenge may have been stored "
                "with equal detail."
            ),
            (
                "Web search is supplementary and must not replace "
                "memory as the primary evidence source."
            ),
        ],
    }

    Path("results").mkdir(exist_ok=True)

    Path("results/challenge_7_evidence.json").write_text(
        json.dumps(output, indent=2, default=str),
        encoding="utf-8",
    )

    print("Challenge 7 complete.")
    print("Primary source: vector_db_search")
    print("Memory success:", memory.get("success"))
    print("Supplementary web success:", web.get("success"))

    memory_data = memory.get("data")

    if isinstance(memory_data, dict):
        results = memory_data.get(
            "results",
            memory_data.get("documents", []),
        )

        if isinstance(results, list):
            print("Memory results retrieved:", len(results))


if __name__ == "__main__":
    main()


