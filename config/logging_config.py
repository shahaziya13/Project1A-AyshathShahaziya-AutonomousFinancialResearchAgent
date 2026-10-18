"""Logging configuration for the Autonomous Financial Research Agent."""

import logging
from pathlib import Path

from config.settings import BASE_DIR, settings


LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "agent.log"


def setup_logging() -> logging.Logger:
    """Configure console and file logging for the application."""

    logger = logging.getLogger("financial_research_agent")
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    # Avoid adding duplicate handlers when called multiple times.
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()


def log_decision(summary: str) -> None:
    """Log a concise agent decision summary."""
    logger.info("DECISION | %s", summary)


def log_tool_call(tool_name: str, arguments: dict) -> None:
    """Log a tool invocation without exposing secrets."""
    logger.info(
        "TOOL_CALL | tool=%s | arguments=%s",
        tool_name,
        arguments,
    )


def log_observation(tool_name: str, success: bool, summary: str) -> None:
    """Log a concise tool-result observation."""
    logger.info(
        "OBSERVATION | tool=%s | success=%s | %s",
        tool_name,
        success,
        summary,
    )


def log_error(component: str, error: Exception | str) -> None:
    """Log an application error."""
    logger.error(
        "ERROR | component=%s | %s",
        component,
        error,
    )