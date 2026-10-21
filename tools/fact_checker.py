from __future__ import annotations

from typing import Any


def fact_checker(
    claim: str,
    evidence: list[dict[str, Any]],
    tolerance_percent: float = 5.0,
) -> dict[str, Any]:
    """
    Verify a claim using evidence from multiple sources.

    For numerical evidence, values are compared and disagreements
    greater than the tolerance percentage are flagged.
    """

    if not claim or not claim.strip():
        raise ValueError("claim cannot be empty.")

    if not evidence:
        raise ValueError(
            "At least one evidence item is required."
        )

    if tolerance_percent < 0:
        raise ValueError(
            "tolerance_percent cannot be negative."
        )

    numerical_evidence = []
    supporting_sources = []
    conflicting_sources = []

    for item in evidence:
        source = str(
            item.get("source", "Unknown source")
        )

        supports_claim = item.get("supports_claim")

        if supports_claim is True:
            supporting_sources.append(source)
        elif supports_claim is False:
            conflicting_sources.append(source)

        value = item.get("value")

        if isinstance(value, (int, float)):
            numerical_evidence.append(
                {
                    "source": source,
                    "value": float(value),
                }
            )

    numerical_conflict = False
    max_disagreement_percent = 0.0

    if len(numerical_evidence) >= 2:
        values = [
            item["value"]
            for item in numerical_evidence
        ]

        minimum = min(values)
        maximum = max(values)

        if maximum == 0:
            disagreement = 0.0
        else:
            disagreement = (
                abs(maximum - minimum)
                / abs(maximum)
            ) * 100

        max_disagreement_percent = disagreement

        if disagreement > tolerance_percent:
            numerical_conflict = True

    if conflicting_sources or numerical_conflict:
        status = "conflicting"
        verified = False

    elif supporting_sources:
        status = "supported"
        verified = True

    else:
        status = "insufficient_evidence"
        verified = False

    return {
        "success": True,
        "tool": "fact_checker",
        "data": {
            "claim": claim.strip(),
            "status": status,
            "verified": verified,
            "supporting_sources": supporting_sources,
            "conflicting_sources": conflicting_sources,
            "numerical_evidence": numerical_evidence,
            "max_disagreement_percent": round(
                max_disagreement_percent,
                4,
            ),
            "tolerance_percent": tolerance_percent,
            "numerical_conflict": numerical_conflict,
            "evidence_count": len(evidence),
        },
        "source": "ARA-1 Cross-Source Verification Engine",
        "confidence": (
            0.95
            if len(evidence) >= 2
            else 0.70
        ),
    }