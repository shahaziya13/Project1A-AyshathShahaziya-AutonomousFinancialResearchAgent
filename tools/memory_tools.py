from __future__ import annotations

from typing import Any

from memory.vector_store import vector_store


def vector_db_store(
    text: str,
    company: str,
    source: str,
    source_type: str = "research",
    research_query: str = "",
    confidence: float = 0.8,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Store research evidence in ARA-1 long-term memory."""

    try:
        result = vector_store.store(
            text=text,
            company=company,
            source=source,
            source_type=source_type,
            research_query=research_query,
            confidence=confidence,
            metadata=metadata,
        )

        return {
            "success": True,
            "tool": "vector_db_store",
            "data": result,
            "source": "ARA-1 ChromaDB Long-Term Memory",
            "confidence": 1.0,
        }

    except Exception as error:
        return {
            "success": False,
            "tool": "vector_db_store",
            "error": str(error),
            "error_type": type(error).__name__,
        }


def vector_db_search(
    query: str,
    n_results: int = 5,
    company: str | None = None,
) -> dict[str, Any]:
    """Search previously stored research evidence."""

    try:
        result = vector_store.search(
            query=query,
            n_results=n_results,
            company=company,
        )

        return {
            "success": True,
            "tool": "vector_db_search",
            "data": result,
            "source": "ARA-1 ChromaDB Long-Term Memory",
            "confidence": 0.9,
        }

    except Exception as error:
        return {
            "success": False,
            "tool": "vector_db_search",
            "error": str(error),
            "error_type": type(error).__name__,
        }