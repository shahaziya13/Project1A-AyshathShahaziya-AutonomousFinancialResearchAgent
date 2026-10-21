"""Multi-source evidence synthesis for ARA-1."""

from __future__ import annotations

from collections import defaultdict
from typing import Any


SOURCE_PRIORITY = {
    "SEC EDGAR": 1.00,
    "Company Investor Relations": 0.95,
    "Yahoo Finance via yfinance": 0.85,
    "Financial Data API": 0.85,
    "Tavily Search API": 0.75,
    "Tavily News Search + VADER": 0.70,
    "Vector Memory": 0.65,
    "Unknown": 0.50,
}


class EvidenceSynthesizer:
    """Combine, rank, and summarize evidence from multiple research tools."""

    def source_weight(self, source: str | None) -> float:
        if not source:
            return SOURCE_PRIORITY["Unknown"]

        for known_source, weight in SOURCE_PRIORITY.items():
            if known_source.lower() in source.lower():
                return weight

        return SOURCE_PRIORITY["Unknown"]

    def normalize_evidence(self, evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized = []

        for index, item in enumerate(evidence):
            source = str(item.get("source", "Unknown"))
            confidence = float(item.get("confidence", 0.5))

            confidence = max(0.0, min(confidence, 1.0))
            source_weight = self.source_weight(source)

            normalized.append(
                {
                    "id": item.get("id", f"evidence_{index + 1}"),
                    "claim": str(item.get("claim", "")).strip(),
                    "value": item.get("value"),
                    "source": source,
                    "source_url": item.get("source_url"),
                    "confidence": confidence,
                    "source_weight": source_weight,
                    "reliability_score": round(
                        confidence * source_weight,
                        4,
                    ),
                    "metadata": item.get("metadata", {}),
                }
            )

        return normalized

    def rank_evidence(self, evidence: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized = self.normalize_evidence(evidence)

        return sorted(
            normalized,
            key=lambda item: item["reliability_score"],
            reverse=True,
        )

    def group_by_claim(self, evidence: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
        groups = defaultdict(list)

        for item in self.rank_evidence(evidence):
            claim = item["claim"] or "unspecified_claim"
            groups[claim].append(item)

        return dict(groups)

    def synthesize(self, evidence: list[dict[str, Any]]) -> dict[str, Any]:
        ranked = self.rank_evidence(evidence)
        grouped = self.group_by_claim(evidence)

        sources = {
            item["source"]
            for item in ranked
            if item["source"]
        }

        if ranked:
            overall_confidence = sum(
                item["reliability_score"] for item in ranked
            ) / len(ranked)
        else:
            overall_confidence = 0.0

        return {
            "evidence_count": len(ranked),
            "source_count": len(sources),
            "overall_confidence": round(overall_confidence, 4),
            "ranked_evidence": ranked,
            "claim_groups": grouped,
        }


def synthesize_evidence(evidence: list[dict[str, Any]]) -> dict[str, Any]:
    return EvidenceSynthesizer().synthesize(evidence)
