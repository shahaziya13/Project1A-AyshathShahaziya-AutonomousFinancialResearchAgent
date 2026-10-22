"""Controlled API failure simulation for ARA-1 stress testing."""

from __future__ import annotations

import random
from typing import Any, Callable


class FailureSimulator:
    """Wrap tools with reproducible simulated failures."""

    def __init__(
        self,
        failure_rate: float = 0.5,
        seed: int = 42,
    ):
        if not 0 <= failure_rate <= 1:
            raise ValueError("failure_rate must be between 0 and 1.")

        self.failure_rate = failure_rate
        self.random = random.Random(seed)
        self.attempts = 0
        self.failures = 0
        self.successes = 0

    def execute(
        self,
        tool_name: str,
        tool_function: Callable[..., Any],
        **kwargs: Any,
    ) -> dict[str, Any]:

        self.attempts += 1

        if self.random.random() < self.failure_rate:
            self.failures += 1

            return {
                "success": False,
                "tool": tool_name,
                "simulated_failure": True,
                "error": "Simulated API failure for resilience testing.",
                "data": None,
            }

        try:
            result = tool_function(**kwargs)
            self.successes += 1

            return {
                "success": True,
                "tool": tool_name,
                "simulated_failure": False,
                "data": result,
            }

        except Exception as exc:
            self.failures += 1

            return {
                "success": False,
                "tool": tool_name,
                "simulated_failure": False,
                "error": str(exc),
                "data": None,
            }

    def statistics(self) -> dict[str, Any]:
        actual_failure_rate = (
            self.failures / self.attempts
            if self.attempts
            else 0.0
        )

        return {
            "configured_failure_rate": self.failure_rate,
            "attempts": self.attempts,
            "failures": self.failures,
            "successes": self.successes,
            "observed_failure_rate": round(actual_failure_rate, 4),
        }
