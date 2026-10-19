"""Shared utilities for external financial research APIs."""

import hashlib
import json
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class CacheEntry:
    """A cached API response."""

    value: Any
    expires_at: float


class TTLCache:
    """Simple in-memory cache with time-based expiration."""

    def __init__(self, ttl_seconds: int = 300) -> None:
        if ttl_seconds <= 0:
            raise ValueError("ttl_seconds must be greater than zero.")

        self.ttl_seconds = ttl_seconds
        self._cache: dict[str, CacheEntry] = {}
        self._lock = threading.Lock()

    @staticmethod
    def make_key(
        namespace: str,
        parameters: dict[str, Any],
    ) -> str:
        """Create a stable cache key."""

        serialized = json.dumps(
            parameters,
            sort_keys=True,
            default=str,
        )

        digest = hashlib.sha256(
            serialized.encode("utf-8")
        ).hexdigest()

        return f"{namespace}:{digest}"

    def get(self, key: str) -> Any | None:
        """Return a cached value when it has not expired."""

        with self._lock:
            entry = self._cache.get(key)

            if entry is None:
                return None

            if time.monotonic() >= entry.expires_at:
                del self._cache[key]
                return None

            return entry.value

    def set(self, key: str, value: Any) -> None:
        """Store a value in the cache."""

        with self._lock:
            self._cache[key] = CacheEntry(
                value=value,
                expires_at=(
                    time.monotonic()
                    + self.ttl_seconds
                ),
            )

    def clear(self) -> None:
        """Clear all cached responses."""

        with self._lock:
            self._cache.clear()


class RateLimiter:
    """Thread-safe minimum-interval API rate limiter."""

    def __init__(
        self,
        requests_per_second: float = 1.0,
    ) -> None:
        if requests_per_second <= 0:
            raise ValueError(
                "requests_per_second must be greater than zero."
            )

        self.minimum_interval = (
            1.0 / requests_per_second
        )

        self._last_request = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        """Wait until another request is allowed."""

        with self._lock:
            now = time.monotonic()

            elapsed = now - self._last_request

            remaining = (
                self.minimum_interval - elapsed
            )

            if remaining > 0:
                time.sleep(remaining)

            self._last_request = time.monotonic()


def cached_api_call(
    namespace: str,
    parameters: dict[str, Any],
    cache: TTLCache,
    rate_limiter: RateLimiter,
    request_function: Callable[[], Any],
) -> tuple[Any, bool]:
    """
    Execute a cached and rate-limited API request.

    Returns:
        tuple:
            response value,
            whether the response came from cache.
    """

    key = cache.make_key(
        namespace,
        parameters,
    )

    cached_value = cache.get(key)

    if cached_value is not None:
        return cached_value, True

    rate_limiter.wait()

    value = request_function()

    cache.set(
        key,
        value,
    )

    return value, False


api_cache = TTLCache(
    ttl_seconds=300,
)