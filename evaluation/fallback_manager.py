"""Fallback and graceful-degradation handling for ARA-1."""

from __future__ import annotations

from typing import Any, Callable


class FallbackManager:
    """Execute a primary source followed by fallback sources."""

    def execute_chain(
        self,
        primary_name: str,
        primary: Callable[[], dict[str, Any]],
        fallbacks: list[tuple[str, Callable[[], dict[str, Any]]]],
    ) -> dict[str, Any]:

        attempts = []

        try:
            result = primary()

            attempts.append(
                {
                    "source": primary_name,
                    "success": bool(result.get("success", False)),
                }
            )

            if result.get("success"):
                return {
                    "success": True,
                    "used_source": primary_name,
                    "fallback_used": False,
                    "result": result,
                    "attempts": attempts,
                    "data_gap": None,
                }

        except Exception as exc:
            attempts.append(
                {
                    "source": primary_name,
                    "success": False,
                    "error": str(exc),
                }
            )

        for name, fallback in fallbacks:
            try:
                result = fallback()

                attempts.append(
                    {
                        "source": name,
                        "success": bool(result.get("success", False)),
                    }
                )

                if result.get("success"):
                    return {
                        "success": True,
                        "used_source": name,
                        "fallback_used": True,
                        "result": result,
                        "attempts": attempts,
                        "data_gap": (
                            f"Primary source {primary_name} was unavailable; "
                            f"{name} was used as fallback."
                        ),
                    }

            except Exception as exc:
                attempts.append(
                    {
                        "source": name,
                        "success": False,
                        "error": str(exc),
                    }
                )

        return {
            "success": False,
            "used_source": None,
            "fallback_used": bool(fallbacks),
            "result": None,
            "attempts": attempts,
            "data_gap": (
                f"No usable evidence was obtained from {primary_name} "
                "or configured fallback sources."
            ),
        }
