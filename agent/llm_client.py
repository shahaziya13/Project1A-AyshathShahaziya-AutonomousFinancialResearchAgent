"""LLM client with retry logic and token usage tracking."""

from dataclasses import dataclass, asdict
from typing import Optional

from openai import OpenAI
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from config.logging_config import log_error, logger
from config.settings import settings


@dataclass
class TokenUsage:
    """Track token usage across LLM requests."""

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    requests: int = 0

    def add(
        self,
        input_tokens: int,
        output_tokens: int,
        total_tokens: int,
    ) -> None:
        """Add token usage from one request."""

        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.total_tokens += total_tokens
        self.requests += 1

    def to_dict(self) -> dict:
        """Return usage statistics as a dictionary."""
        return asdict(self)


class LLMClient:
    """Wrapper around supported LLM providers."""

    def __init__(self) -> None:
        """Initialize the configured LLM provider."""

        self.provider = settings.llm_provider.lower()
        self.model = settings.openai_model
        self.token_usage = TokenUsage()
        self.client: Optional[OpenAI] = None

        if self.provider == "openai":
            if not settings.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY is required when "
                    "LLM_PROVIDER=openai."
                )

            self.client = OpenAI(
                api_key=settings.openai_api_key,
            )

        elif self.provider != "mock":
            raise ValueError(
                f"Unsupported LLM provider: {self.provider}"
            )

        logger.info(
            "LLM_CLIENT | provider=%s | model=%s",
            self.provider,
            self.model,
        )

    @retry(
        retry=retry_if_exception_type(Exception),
        stop=stop_after_attempt(settings.llm_max_retries),
        wait=wait_exponential_jitter(
            initial=settings.llm_retry_min_seconds,
            max=settings.llm_retry_max_seconds,
        ),
        reraise=True,
    )
    def _openai_request(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ):
        """Send a request to OpenAI with automatic retries."""

        if self.client is None:
            raise RuntimeError("OpenAI client is not initialized.")

        input_messages = []

        if system_prompt:
            input_messages.append(
                {
                    "role": "system",
                    "content": system_prompt,
                }
            )

        input_messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        return self.client.responses.create(
            model=self.model,
            input=input_messages,
            max_output_tokens=settings.llm_max_output_tokens,
        )

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """Generate text using the configured provider."""

        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        if self.provider == "mock":
            response_text = (
                "[MOCK LLM RESPONSE] "
                f"Received research request: {prompt}"
            )

            # Mock token values allow us to test tracking.
            input_tokens = max(1, len(prompt.split()))
            output_tokens = max(1, len(response_text.split()))
            total_tokens = input_tokens + output_tokens

            self.token_usage.add(
                input_tokens,
                output_tokens,
                total_tokens,
            )

            logger.info(
                "LLM_REQUEST | provider=mock | "
                "input_tokens=%s | output_tokens=%s",
                input_tokens,
                output_tokens,
            )

            return response_text

        try:
            response = self._openai_request(
                prompt=prompt,
                system_prompt=system_prompt,
            )

            usage = response.usage

            input_tokens = getattr(
                usage,
                "input_tokens",
                0,
            ) or 0

            output_tokens = getattr(
                usage,
                "output_tokens",
                0,
            ) or 0

            total_tokens = getattr(
                usage,
                "total_tokens",
                input_tokens + output_tokens,
            ) or (input_tokens + output_tokens)

            self.token_usage.add(
                input_tokens,
                output_tokens,
                total_tokens,
            )

            logger.info(
                "LLM_REQUEST | provider=openai | "
                "model=%s | input_tokens=%s | "
                "output_tokens=%s",
                self.model,
                input_tokens,
                output_tokens,
            )

            return response.output_text

        except Exception as exc:
            log_error("LLMClient", exc)
            raise

    def get_token_usage(self) -> dict:
        """Return cumulative LLM token usage."""
        return self.token_usage.to_dict()

    def reset_token_usage(self) -> None:
        """Reset accumulated token statistics."""
        self.token_usage = TokenUsage()


llm_client = LLMClient()