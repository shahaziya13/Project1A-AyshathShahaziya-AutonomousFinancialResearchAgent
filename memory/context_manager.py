from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ContextItem:
    """One item stored in the agent's short-term working memory."""

    content: str
    importance: float = 0.5
    metadata: dict[str, Any] = field(default_factory=dict)


class ContextManager:
    """
    Short-term memory manager for ARA-1.

    Keeps important findings available during a research session
    and reduces context size when the configured limit is reached.
    """

    def __init__(self, max_characters: int = 12000) -> None:
        if max_characters <= 0:
            raise ValueError(
                "max_characters must be greater than zero."
            )

        self.max_characters = max_characters
        self.items: list[ContextItem] = []

    def add(
        self,
        content: str,
        importance: float = 0.5,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Add a finding to short-term memory."""

        if not content or not content.strip():
            raise ValueError("content cannot be empty.")

        if not 0.0 <= importance <= 1.0:
            raise ValueError(
                "importance must be between 0.0 and 1.0."
            )

        self.items.append(
            ContextItem(
                content=content.strip(),
                importance=importance,
                metadata=metadata or {},
            )
        )

        if self.character_count() > self.max_characters:
            self.compress()

    def character_count(self) -> int:
        """Return approximate context size in characters."""

        return sum(
            len(item.content)
            for item in self.items
        )

    def compress(self) -> None:
        """
        Reduce working memory while retaining important findings.

        Higher-importance findings are retained first.
        """

        if not self.items:
            return

        ordered_items = sorted(
            self.items,
            key=lambda item: item.importance,
            reverse=True,
        )

        retained: list[ContextItem] = []
        current_size = 0

        target_size = int(self.max_characters * 0.7)

        for item in ordered_items:
            item_size = len(item.content)

            if current_size + item_size <= target_size:
                retained.append(item)
                current_size += item_size

        self.items = retained

    def get_context(self) -> str:
        """Return current short-term context for the agent."""

        if not self.items:
            return ""

        ordered_items = sorted(
            self.items,
            key=lambda item: item.importance,
            reverse=True,
        )

        return "\n\n".join(
            item.content
            for item in ordered_items
        )

    def get_items(self) -> list[ContextItem]:
        """Return a copy of the current context items."""

        return list(self.items)

    def clear(self) -> None:
        """Clear the current research-session memory."""

        self.items.clear()


context_manager = ContextManager()