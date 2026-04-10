"""
PSYCHE Cache Layer — Upstash Redis.

Caches:
- ESIE listener state (90s TTL)
- SEA explanations (1h TTL)
- FAISS search results (5min TTL)
- Cold start interview state (30min TTL)
"""

import json
import logging
from typing import Any, Optional

from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class PsycheCache:
    """Redis-backed cache for PSYCHE hot data."""

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()
        self._client = None

    def _get_client(self):
        """Lazy-init Upstash Redis client."""
        if self._client is None:
            try:
                from upstash_redis import Redis
                self._client = Redis(
                    url=self._config.upstash.redis_url,
                    token=self._config.upstash.redis_token,
                )
            except ImportError:
                logger.warning("upstash-redis not installed — cache unavailable")
            except Exception as e:
                logger.error(f"Failed to create Redis client: {e}")
        return self._client

    def get(self, key: str) -> Optional[Any]:
        """Get a cached value."""
        client = self._get_client()
        if client is None:
            return None
        try:
            value = client.get(key)
            if value is not None:
                return json.loads(value)
        except Exception as e:
            logger.debug(f"Cache miss for {key}: {e}")
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 300) -> bool:
        """Set a cached value with TTL."""
        client = self._get_client()
        if client is None:
            return False
        try:
            client.set(key, json.dumps(value), ex=ttl_seconds)
            return True
        except Exception as e:
            logger.error(f"Cache set failed for {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete a cached value."""
        client = self._get_client()
        if client is None:
            return False
        try:
            client.delete(key)
            return True
        except Exception as e:
            logger.error(f"Cache delete failed for {key}: {e}")
            return False

    # --- Domain-specific cache methods ---

    def cache_listener_state(self, user_id: str, state: dict) -> bool:
        """Cache ESIE listener state (90s TTL)."""
        return self.set(f"listener_state:{user_id}", state, ttl_seconds=90)

    def get_listener_state(self, user_id: str) -> Optional[dict]:
        """Get cached listener state."""
        return self.get(f"listener_state:{user_id}")

    def cache_explanation(self, track_id: str, user_id: str, explanation: str) -> bool:
        """Cache SEA explanation (1h TTL)."""
        return self.set(
            f"explanation:{user_id}:{track_id}",
            {"explanation": explanation},
            ttl_seconds=3600,
        )

    def get_explanation(self, track_id: str, user_id: str) -> Optional[str]:
        """Get cached explanation."""
        result = self.get(f"explanation:{user_id}:{track_id}")
        return result["explanation"] if result else None

    def cache_cold_start_state(self, user_id: str, state: dict) -> bool:
        """Cache interview progress (30min TTL)."""
        return self.set(f"cold_start:{user_id}", state, ttl_seconds=1800)

    def get_cold_start_state(self, user_id: str) -> Optional[dict]:
        """Get cold start interview state."""
        return self.get(f"cold_start:{user_id}")
