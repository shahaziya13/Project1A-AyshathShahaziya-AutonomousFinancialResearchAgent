"""Conflict detection and resolution for ARA-1."""

from __future__ import annotations

from typing import Any


class ConflictResolver:
    def __init__(self, tolerance_percent: float = 5.0):
        self.tolerance_percent = tolerance_percent

    def numerical_difference_percent(
        self,
        first: float,
        second: float,
    ) -> float:
        denominator = max(abs(first), abs(second))

        if denominator == 0:
            return 0.0

        return abs(first - second) / denominator * 100

    def detect_numerical_conflict(
        self,
        values: list[dict[str, Any]],
    ) -> dict[str, Any]:
        numeric = [
            item
            for item in values
            if isinstance(item.get("value"), (int, float))
        ]

        conflicts = []

        for i in range(len(numeric)):
            for j in range(i + 1, len(numeric)):
                first = numeric[i]
                second = numeric[j]

                difference = self.numerical_difference_percent(
                    float(first["value"]),
                    float(second["value"]),
                )

                if difference > self.tolerance_percent:
                    conflicts.append(
                        {
                            "source_1": first.get("source"),
                            "value_1": first["value"],
                            "source_2": second.get("source"),
                            "value_2": second["value"],
                            "difference_percent": round(difference, 2),
                        }
                    )

        return {
            "has_conflict": bool(conflicts),
            "tolerance_percent": self.tolerance_percent,
            "conflicts": conflicts,
        }

    def resolve(
        self,
        evidence: list[dict[str, Any]],
    ) -> dict[str, Any]:
        if not evidence:
            return {
                "status": "insufficient_evidence",
                "selected": None,
                "alternatives": [],
            }

        ranked = sorted(
            evidence,
            key=lambda item: (
                item.get("reliability_score", 0),
                item.get("confidence", 0),
            ),
            reverse=True,
        )

        numerical = self.detect_numerical_conflict(ranked)

        return {
            "status": (
                "conflict_resolved"
                if numerical["has_conflict"]
                else "consistent"
            ),
            "selected": ranked[0],
            "alternatives": ranked[1:],
            "numerical_conflict": numerical,
            "resolution_reason": (
                "Selected the evidence with the highest "
                "source-weighted reliability score."
            ),
        }


def resolve_conflict(
    evidence: list[dict[str, Any]],
    tolerance_percent: float = 5.0,
) -> dict[str, Any]:
    return ConflictResolver(tolerance_percent).resolve(evidence)
