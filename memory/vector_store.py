from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

import chromadb

from config.settings import settings


class VectorStore:
    """
    Long-term vector memory for ARA-1.

    Stores research evidence in ChromaDB and supports semantic retrieval
    with metadata attached to each stored chunk.
    """

    def __init__(self) -> None:
        self.client = chromadb.PersistentClient(
            path=str(settings.chroma_persist_directory)
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={
                "description": (
                    "Long-term memory for financial research evidence"
                )
            },
        )

    @staticmethod
    def chunk_text(
        text: str,
        chunk_size: int = 1000,
        overlap: int = 150,
    ) -> list[str]:
        """Split text into overlapping chunks."""

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than zero.")

        if overlap < 0:
            raise ValueError("overlap cannot be negative.")

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size."
            )

        clean_text = " ".join(text.split())

        chunks: list[str] = []
        start = 0

        while start < len(clean_text):
            end = min(start + chunk_size, len(clean_text))
            chunk = clean_text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end >= len(clean_text):
                break

            start = end - overlap

        return chunks

    @staticmethod
    def _document_id(
        company: str,
        source: str,
        text: str,
        chunk_index: int,
    ) -> str:
        """Create a deterministic identifier for a memory chunk."""

        raw_value = (
            f"{company}|{source}|{chunk_index}|{text}"
        )

        return hashlib.sha256(
            raw_value.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _clean_metadata(
        metadata: dict[str, Any],
    ) -> dict[str, str | int | float | bool]:
        """
        Convert metadata into values supported by ChromaDB.
        """

        cleaned: dict[str, str | int | float | bool] = {}

        for key, value in metadata.items():
            if value is None:
                continue

            if isinstance(value, (str, int, float, bool)):
                cleaned[key] = value
            else:
                cleaned[key] = str(value)

        return cleaned

    def store(
        self,
        text: str,
        company: str,
        source: str,
        source_type: str = "research",
        research_query: str = "",
        confidence: float = 0.8,
        metadata: dict[str, Any] | None = None,
        chunk_size: int = 1000,
        overlap: int = 150,
    ) -> dict[str, Any]:
        """
        Chunk and store research evidence in long-term memory.
        """

        if not company.strip():
            raise ValueError("company cannot be empty.")

        if not source.strip():
            raise ValueError("source cannot be empty.")

        if not 0.0 <= confidence <= 1.0:
            raise ValueError(
                "confidence must be between 0.0 and 1.0."
            )

        chunks = self.chunk_text(
            text=text,
            chunk_size=chunk_size,
            overlap=overlap,
        )

        timestamp = datetime.now(timezone.utc).isoformat()

        ids: list[str] = []
        metadatas: list[dict[str, Any]] = []

        for index, chunk in enumerate(chunks):
            chunk_metadata: dict[str, Any] = {
                "company": company,
                "source": source,
                "source_type": source_type,
                "research_query": research_query,
                "confidence": confidence,
                "timestamp": timestamp,
                "chunk_index": index,
            }

            if metadata:
                chunk_metadata.update(metadata)

            cleaned_metadata = self._clean_metadata(
                chunk_metadata
            )

            document_id = self._document_id(
                company=company,
                source=source,
                text=chunk,
                chunk_index=index,
            )

            ids.append(document_id)
            metadatas.append(cleaned_metadata)

        self.collection.upsert(
            ids=ids,
            documents=chunks,
            metadatas=metadatas,
        )

        return {
            "success": True,
            "stored_chunks": len(chunks),
            "ids": ids,
            "company": company,
            "source": source,
        }

    def search(
        self,
        query: str,
        n_results: int = 5,
        company: str | None = None,
    ) -> dict[str, Any]:
        """
        Retrieve relevant research evidence from long-term memory.
        """

        if not query or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if n_results < 1:
            raise ValueError(
                "n_results must be at least 1."
            )

        total_documents = self.collection.count()

        if total_documents == 0:
            return {
                "success": True,
                "query": query,
                "results": [],
                "count": 0,
            }

        requested_results = min(
            n_results,
            total_documents,
        )

        where = None

        if company:
            where = {
                "company": {
                    "$eq": company
                }
            }

        response = self.collection.query(
            query_texts=[query],
            n_results=requested_results,
            where=where,
            include=[
                "documents",
                "metadatas",
                "distances",
            ],
        )

        documents = response.get("documents", [[]])[0]
        metadatas = response.get("metadatas", [[]])[0]
        distances = response.get("distances", [[]])[0]
        ids = response.get("ids", [[]])[0]

        results: list[dict[str, Any]] = []

        for document_id, document, item_metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):
            results.append(
                {
                    "id": document_id,
                    "text": document,
                    "metadata": item_metadata,
                    "distance": distance,
                }
            )

        return {
            "success": True,
            "query": query,
            "results": results,
            "count": len(results),
        }

    def count(self) -> int:
        """Return the number of stored memory chunks."""

        return self.collection.count()


vector_store = VectorStore()