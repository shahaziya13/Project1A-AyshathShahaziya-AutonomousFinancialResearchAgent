"""RAG pipeline for grounded financial research."""

from __future__ import annotations

from typing import Any


class RAGPipeline:
    """Transform queries, rank retrieved evidence, and assemble context."""

    def transform_query(
        self,
        query: str,
        company: str | None = None,
    ) -> list[str]:
        query = query.strip()

        queries = [query]

        if company:
            queries.extend(
                [
                    f"{company} {query}",
                    f"{company} financial performance {query}",
                    f"{company} SEC filing {query}",
                ]
            )

        # Remove duplicates while preserving order.
        return list(dict.fromkeys(queries))

    def rerank(
        self,
        documents: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        ranked = []

        for document in documents:
            similarity = float(
                document.get(
                    "similarity",
                    document.get("score", 0.5),
                )
            )

            confidence = float(document.get("confidence", 0.7))

            similarity = max(0.0, min(similarity, 1.0))
            confidence = max(0.0, min(confidence, 1.0))

            final_score = (0.65 * similarity) + (0.35 * confidence)

            item = dict(document)
            item["rerank_score"] = round(final_score, 4)

            ranked.append(item)

        return sorted(
            ranked,
            key=lambda item: item["rerank_score"],
            reverse=True,
        )

    def assemble_context(
        self,
        documents: list[dict[str, Any]],
        max_documents: int = 5,
    ) -> str:
        ranked = self.rerank(documents)[:max_documents]

        if not ranked:
            return "No relevant evidence retrieved."

        blocks = []

        for index, document in enumerate(ranked, start=1):
            text = (
                document.get("text")
                or document.get("content")
                or document.get("document")
                or ""
            )

            source = document.get("source", "Unknown")
            company = document.get("company", "Unknown")

            blocks.append(
                f"[Evidence {index}]\n"
                f"Company: {company}\n"
                f"Source: {source}\n"
                f"Content: {text}\n"
                f"Relevance: {document['rerank_score']}"
            )

        return "\n\n".join(blocks)

    def build_grounded_package(
        self,
        query: str,
        documents: list[dict[str, Any]],
        company: str | None = None,
        max_documents: int = 5,
    ) -> dict[str, Any]:
        transformed_queries = self.transform_query(
            query,
            company,
        )

        ranked = self.rerank(documents)

        selected = ranked[:max_documents]

        return {
            "original_query": query,
            "transformed_queries": transformed_queries,
            "retrieved_count": len(documents),
            "selected_count": len(selected),
            "selected_documents": selected,
            "context": self.assemble_context(
                selected,
                max_documents,
            ),
            "grounding_status": (
                "grounded"
                if selected
                else "insufficient_evidence"
            ),
        }
