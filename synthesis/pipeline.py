"""End-to-end evidence synthesis pipeline for ARA-1."""

from __future__ import annotations

from typing import Any

from synthesis.synthesizer import EvidenceSynthesizer
from synthesis.conflict_resolver import ConflictResolver


class SynthesisPipeline:
    """Rank evidence, detect conflicts, and produce grounded conclusions."""

    def __init__(self, tolerance_percent: float = 5.0):
        self.synthesizer = EvidenceSynthesizer()
        self.resolver = ConflictResolver(tolerance_percent)

    def run(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        synthesis = self.synthesizer.synthesize(evidence)

        resolutions = {}

        for claim, claim_evidence in synthesis["claim_groups"].items():
            resolutions[claim] = self.resolver.resolve(claim_evidence)

        conflicts = [
            claim
            for claim, result in resolutions.items()
            if result["status"] == "conflict_resolved"
        ]

        return {
            "status": "success",
            "evidence_count": synthesis["evidence_count"],
            "source_count": synthesis["source_count"],
            "overall_confidence": synthesis["overall_confidence"],
            "claim_resolutions": resolutions,
            "conflicting_claims": conflicts,
            "conflict_count": len(conflicts),
            "limitations": self._limitations(synthesis),
        }

    def _limitations(self, synthesis: dict[str, Any]) -> list[str]:
        limitations = []

        if synthesis["evidence_count"] == 0:
            limitations.append("No evidence was available.")

        if synthesis["source_count"] < 2 and synthesis["evidence_count"] > 0:
            limitations.append(
                "Only one source was available; independent verification is limited."
            )

        if synthesis["overall_confidence"] < 0.6:
            limitations.append(
                "Overall source-weighted confidence is below 0.60."
            )

        return limitations


def synthesize_research(
    evidence: list[dict[str, Any]],
    tolerance_percent: float = 5.0,
) -> dict[str, Any]:
    return SynthesisPipeline(tolerance_percent).run(evidence)
