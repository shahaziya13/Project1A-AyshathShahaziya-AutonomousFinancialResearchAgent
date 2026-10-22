"""Performance and tool-efficiency monitoring for ARA-1."""

from __future__ import annotations

import time
from typing import Any, Callable


class PerformanceMonitor:
    """Track execution time, tool usage, success, and usefulness."""

    def __init__(self):
        self.records: list[dict[str, Any]] = []

    def track(
        self,
        tool_name: str,
        function: Callable[..., Any],
        *args: Any,
        useful: bool = True,
        **kwargs: Any,
    ) -> Any:

        start = time.perf_counter()
        success = True
        error = None

        try:
            result = function(*args, **kwargs)

            if isinstance(result, dict):
                success = bool(result.get("success", True))

            return result

        except Exception as exc:
            success = False
            error = str(exc)
            raise

        finally:
            elapsed = time.perf_counter() - start

            self.records.append(
                {
                    "tool": tool_name,
                    "success": success,
                    "useful": useful,
                    "duration_seconds": round(elapsed, 6),
                    "error": error,
                }
            )

    def summary(self) -> dict[str, Any]:
        total = len(self.records)

        if total == 0:
            return {
                "total_calls": 0,
                "successful_calls": 0,
                "useful_calls": 0,
                "tool_success_rate": 0.0,
                "tool_efficiency": 0.0,
                "average_duration_seconds": 0.0,
                "target_met": False,
            }

        successful = sum(
            1 for record in self.records
            if record["success"]
        )

        useful = sum(
            1 for record in self.records
            if record["useful"]
        )

        total_duration = sum(
            record["duration_seconds"]
            for record in self.records
        )

        efficiency = useful / total

        return {
            "total_calls": total,
            "successful_calls": successful,
            "useful_calls": useful,
            "tool_success_rate": round(successful / total, 4),
            "tool_efficiency": round(efficiency, 4),
            "average_duration_seconds": round(
                total_duration / total,
                6,
            ),
            "target_met": efficiency >= 0.70,
        }


class ToolCallOptimizer:
    """Avoid redundant identical tool calls during one research run."""

    def __init__(self):
        self._cache: dict[str, Any] = {}
        self.cache_hits = 0
        self.cache_misses = 0

    def _key(
        self,
        tool_name: str,
        arguments: dict[str, Any],
    ) -> str:
        normalized = repr(
            sorted(arguments.items(), key=lambda item: item[0])
        )
        return f"{tool_name}:{normalized}"

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        function: Callable[[dict[str, Any]], Any],
    ) -> Any:

        key = self._key(tool_name, arguments)

        if key in self._cache:
            self.cache_hits += 1
            return self._cache[key]

        self.cache_misses += 1
        result = function(arguments)
        self._cache[key] = result

        return result

    def statistics(self) -> dict[str, Any]:
        total = self.cache_hits + self.cache_misses

        return {
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "total_requests": total,
            "duplicate_calls_avoided": self.cache_hits,
            "cache_hit_rate": round(
                self.cache_hits / total,
                4,
            ) if total else 0.0,
        }
