"""Post-generation verification for ARA-1."""

from __future__ import annotations

from typing import Any


class ResearchVerifier:
    """Verify research claims against collected evidence."""

    def __init__(self, minimum_confidence: float = 0.60):
        self.minimum_confidence = minimum_confidence

    def verify_claim(
        self,
        claim: str,
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:

        if not evidence:
            return {
                "claim": claim,
                "status": "unsupported",
                "confidence": 0.0,
                "supporting_sources": [],
                "reason": "No supporting evidence was supplied.",
            }

        supporting = [
            item
            for item in evidence
            if item.get("supports_claim", True)
        ]

        contradicting = [
            item
            for item in evidence
            if item.get("supports_claim") is False
        ]

        if not supporting:
            return {
                "claim": claim,
                "status": "contradicted" if contradicting else "unsupported",
                "confidence": 0.0,
                "supporting_sources": [],
                "reason": "No source supports the claim.",
            }

        confidence = sum(
            float(item.get("confidence", 0.5))
            for item in supporting
        ) / len(supporting)

        sources = list(
            dict.fromkeys(
                str(item.get("source", "Unknown"))
                for item in supporting
            )
        )

        if contradicting:
            status = "conflicting"
        elif confidence >= self.minimum_confidence:
            status = "verified"
        else:
            status = "low_confidence"

        return {
            "claim": claim,
            "status": status,
            "confidence": round(confidence, 4),
            "supporting_sources": sources,
            "contradicting_sources": [
                str(item.get("source", "Unknown"))
                for item in contradicting
            ],
        }

    def verify_report(
        self,
        claims: list[dict[str, Any]],
    ) -> dict[str, Any]:

        results = []

        for item in claims:
            results.append(
                self.verify_claim(
                    item.get("claim", ""),
                    item.get("evidence", []),
                )
            )

        total = len(results)

        verified = sum(
            result["status"] == "verified"
            for result in results
        )

        problematic = [
            result
            for result in results
            if result["status"] != "verified"
        ]

        verification_rate = (
            verified / total
            if total
            else 0.0
        )

        return {
            "total_claims": total,
            "verified_claims": verified,
            "verification_rate": round(
                verification_rate,
                4,
            ),
            "passed": (
                verification_rate >= 0.90
                if total
                else False
            ),
            "results": results,
            "problematic_claims": problematic,
        }


def verify_research(
    claims: list[dict[str, Any]],
) -> dict[str, Any]:
    return ResearchVerifier().verify_report(claims)
