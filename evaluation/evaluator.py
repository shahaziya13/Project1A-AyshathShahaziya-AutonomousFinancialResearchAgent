"""Evaluation runner for ARA-1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from evaluation.metrics import ResearchEvaluator


class EvaluationRunner:
    def __init__(self):
        self.evaluator = ResearchEvaluator()

    def run(
        self,
        name: str,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        result = self.evaluator.evaluate(data)

        return {
            "evaluation_name": name,
            **result,
        }

    def save(
        self,
        result: dict[str, Any],
        path: str,
    ) -> None:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)

        output.write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )
