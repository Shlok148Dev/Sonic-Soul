"""
PSYCHE Database Layer — User profiles, Sonic Genomes, and session data.

Uses Supabase (PostgreSQL) for persistent storage.
All queries use parameterized inputs to prevent injection.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class PsycheDB:
    """
    Database interface for PSYCHE user data.
    Backed by Supabase (PostgreSQL via REST API).
    """

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()
        self._client = None

    def _get_client(self):
        """Lazy-init Supabase client."""
        if self._client is None:
            try:
                from supabase import create_client
                self._client = create_client(
                    self._config.supabase.url,
                    self._config.supabase.anon_key,
                )
            except ImportError:
                logger.warning("supabase-py not installed — DB operations unavailable")
            except Exception as e:
                logger.error(f"Failed to create Supabase client: {e}")
        return self._client

    async def save_sonic_genome(self, user_id: str, genome: Dict[str, Any]) -> bool:
        """Save or update a user's Sonic Genome."""
        client = self._get_client()
        if client is None:
            logger.warning("No DB client — Sonic Genome not saved")
            return False

        try:
            data = {
                "user_id": user_id,
                "genome": json.dumps(genome),
                "updated_at": datetime.utcnow().isoformat(),
            }
            result = client.table("sonic_genomes").upsert(data).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Failed to save Sonic Genome: {e}")
            return False

    async def get_sonic_genome(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a user's Sonic Genome."""
        client = self._get_client()
        if client is None:
            return None

        try:
            result = (
                client.table("sonic_genomes")
                .select("genome")
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            if result.data:
                return json.loads(result.data["genome"])
        except Exception as e:
            logger.debug(f"No Sonic Genome found for {user_id}: {e}")
        return None

    async def save_listening_event(
        self,
        user_id: str,
        track_id: str,
        event_type: str,
        timestamp: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> bool:
        """Record a listening event (play, skip, save, replay)."""
        client = self._get_client()
        if client is None:
            return False

        try:
            data = {
                "user_id": user_id,
                "track_id": track_id,
                "event_type": event_type,
                "timestamp": timestamp or datetime.utcnow().isoformat(),
                "metadata": json.dumps(metadata or {}),
            }
            result = client.table("listening_events").insert(data).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Failed to save listening event: {e}")
            return False

    async def get_listening_history(
        self,
        user_id: str,
        limit: int = 100,
        event_types: Optional[List[str]] = None,
    ) -> List[Dict]:
        """Get a user's recent listening history."""
        client = self._get_client()
        if client is None:
            return []

        try:
            query = (
                client.table("listening_events")
                .select("*")
                .eq("user_id", user_id)
                .order("timestamp", desc=True)
                .limit(limit)
            )
            if event_types:
                query = query.in_("event_type", event_types)
            result = query.execute()
            return result.data
        except Exception as e:
            logger.error(f"Failed to get listening history: {e}")
            return []

    async def save_cold_start_result(
        self, user_id: str, answers: List[Dict], radar: Dict[str, float]
    ) -> bool:
        """Save cold start interview results."""
        client = self._get_client()
        if client is None:
            return False

        try:
            data = {
                "user_id": user_id,
                "answers": json.dumps(answers),
                "initial_radar": json.dumps(radar),
                "created_at": datetime.utcnow().isoformat(),
            }
            result = client.table("cold_start_results").insert(data).execute()
            return len(result.data) > 0
        except Exception as e:
            logger.error(f"Failed to save cold start results: {e}")
            return False
