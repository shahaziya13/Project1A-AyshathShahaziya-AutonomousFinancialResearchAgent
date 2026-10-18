"""ChromaDB configuration for the financial research agent."""

import chromadb

from config.logging_config import logger
from config.settings import settings


class VectorDatabase:
    """Manage the persistent ChromaDB database."""

    def __init__(self) -> None:
        """Initialize ChromaDB and the research collection."""

        self.client = chromadb.PersistentClient(
            path=settings.chroma_persist_directory
        )

        self.collection = self.client.get_or_create_collection(
            name=settings.chroma_collection_name,
            metadata={
                "description": (
                    "Long-term memory for financial research evidence"
                )
            },
        )

        logger.info(
            "VECTOR_DB | collection=%s | initialized=True",
            settings.chroma_collection_name,
        )

    def get_collection_name(self) -> str:
        """Return the active collection name."""
        return self.collection.name

    def count(self) -> int:
        """Return the number of stored documents."""
        return self.collection.count()


vector_db = VectorDatabase()