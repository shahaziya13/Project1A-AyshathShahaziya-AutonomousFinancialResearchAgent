from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class EpisodicMemory:
    """
    Persistent episodic memory for ARA-1.

    Stores successful research strategies, failures, and recurring
    error patterns so future research sessions can reuse lessons.
    """

    def __init__(
        self,
        file_path: str | Path = "memory/episodic_memory.json",
    ) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        if not self.file_path.exists():
            self._save([])

    def _load(self) -> list[dict[str, Any]]:
        """Load all stored episodes."""

        try:
            with self.file_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                data = json.load(file)

            if isinstance(data, list):
                return data

            return []

        except (json.JSONDecodeError, OSError):
            return []

    def _save(
        self,
        episodes: list[dict[str, Any]],
    ) -> None:
        """Persist episodes to disk."""

        with self.file_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                episodes,
                file,
                indent=2,
                ensure_ascii=False,
            )

    def add_episode(
        self,
        task: str,
        strategy: str,
        outcome: str,
        success: bool,
        lessons: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Store a completed research experience."""

        if not task.strip():
            raise ValueError("task cannot be empty.")

        if not strategy.strip():
            raise ValueError("strategy cannot be empty.")

        if not outcome.strip():
            raise ValueError("outcome cannot be empty.")

        episodes = self._load()

        episode = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "task": task.strip(),
            "strategy": strategy.strip(),
            "outcome": outcome.strip(),
            "success": success,
            "lessons": lessons.strip(),
            "metadata": metadata or {},
        }

        episodes.append(episode)
        self._save(episodes)

        return episode

    def get_episodes(
        self,
        success: bool | None = None,
    ) -> list[dict[str, Any]]:
        """Return stored episodes, optionally filtered."""

        episodes = self._load()

        if success is None:
            return episodes

        return [
            episode
            for episode in episodes
            if episode.get("success") is success
        ]

    def successful_strategies(self) -> list[dict[str, Any]]:
        """Return successful past research experiences."""

        return self.get_episodes(success=True)

    def error_patterns(self) -> list[dict[str, Any]]:
        """Return failed experiences for future avoidance."""

        return self.get_episodes(success=False)

    def count(self) -> int:
        """Return total number of stored episodes."""

        return len(self._load())

    def clear(self) -> None:
        """Remove all stored episodes."""

        self._save([])


episodic_memory = EpisodicMemory()