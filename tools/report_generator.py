from __future__ import annotations

from typing import Any


def report_generator(
    title: str,
    research_query: str,
    sections: list[dict[str, str]],
    sources: list[str] | None = None,
    confidence: float = 0.8,
    limitations: list[str] | None = None,
) -> dict[str, Any]:
    """
    Generate a structured Markdown financial research report.
    """

    if not title or not title.strip():
        raise ValueError("title cannot be empty.")

    if not research_query or not research_query.strip():
        raise ValueError(
            "research_query cannot be empty."
        )

    if not sections:
        raise ValueError(
            "At least one report section is required."
        )

    if not 0 <= confidence <= 1:
        raise ValueError(
            "confidence must be between 0 and 1."
        )

    sources = sources or []
    limitations = limitations or []

    lines: list[str] = []

    lines.append(f"# {title.strip()}")
    lines.append("")

    lines.append("## Research Query")
    lines.append("")
    lines.append(research_query.strip())
    lines.append("")

    lines.append("## Executive Summary")
    lines.append("")
    lines.append(
        "This report was generated from the evidence "
        "collected by the Autonomous Financial Research Agent."
    )
    lines.append("")

    for section in sections:
        heading = section.get(
            "heading",
            "Research Finding",
        ).strip()

        content = section.get(
            "content",
            "",
        ).strip()

        if not content:
            continue

        lines.append(f"## {heading}")
        lines.append("")
        lines.append(content)
        lines.append("")

    lines.append("## Confidence")
    lines.append("")
    lines.append(
        f"Overall confidence score: {confidence:.2f}"
    )
    lines.append("")

    if limitations:
        lines.append("## Limitations")
        lines.append("")

        for limitation in limitations:
            lines.append(f"- {limitation}")

        lines.append("")

    if sources:
        lines.append("## Sources")
        lines.append("")

        for index, source in enumerate(
            sources,
            start=1,
        ):
            lines.append(
                f"{index}. {source}"
            )

        lines.append("")

    markdown_report = "\n".join(lines)

    return {
        "success": True,
        "tool": "report_generator",
        "data": {
            "title": title.strip(),
            "research_query": research_query.strip(),
            "markdown": markdown_report,
            "section_count": len(sections),
            "source_count": len(sources),
            "confidence": confidence,
            "limitations": limitations,
        },
        "source": "ARA-1 Structured Report Generator",
        "confidence": 1.0,
    }