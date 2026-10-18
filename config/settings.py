"""Central configuration management for the financial research agent."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load variables from .env if the file exists.
load_dotenv(BASE_DIR / ".env")


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = os.getenv(
        "APP_NAME",
        "Autonomous Financial Research Agent",
    )
    environment: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # LLM
    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5.6")
    llm_temperature: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    llm_max_output_tokens: int = int(
        os.getenv("LLM_MAX_OUTPUT_TOKENS", "2000")
    )

    # LLM retry settings
    llm_max_retries: int = int(os.getenv("LLM_MAX_RETRIES", "5"))
    llm_retry_min_seconds: float = float(
        os.getenv("LLM_RETRY_MIN_SECONDS", "1")
    )
    llm_retry_max_seconds: float = float(
        os.getenv("LLM_RETRY_MAX_SECONDS", "16")
    )

    # Vector database
    chroma_persist_directory: str = os.getenv(
        "CHROMA_PERSIST_DIRECTORY",
        str(BASE_DIR / "chromadb_data"),
    )
    chroma_collection_name: str = os.getenv(
        "CHROMA_COLLECTION_NAME",
        "financial_research_memory",
    )

    # External APIs - used from Day 5 onward
    alpha_vantage_api_key: str = os.getenv(
        "ALPHA_VANTAGE_API_KEY",
        "",
    )
    fmp_api_key: str = os.getenv("FMP_API_KEY", "")
    tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")
    news_api_key: str = os.getenv("NEWS_API_KEY", "")

    # SEC EDGAR
    sec_user_agent: str = os.getenv(
        "SEC_USER_AGENT",
        "ARA-1 Financial Research Agent",
    )


settings = Settings()