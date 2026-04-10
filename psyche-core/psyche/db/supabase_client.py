"""
Supabase Database Client integration.

Provides direct connectivity to PostgreSQL over the Supabase Python SDK
to store tracking metrics, user trajectories, and genomic preferences.
"""

import logging
from typing import Optional, Dict, Any
from supabase import create_client, Client
from pydantic import BaseModel

from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)

class PsycheDBClient:
    """Manages the Supabase PostgreSQL connection pool."""

    _instance: Optional["PsycheDBClient"] = None

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()
        
        self.supabase: Optional[Client] = None
        
        url = self._config.db.supabase_url
        key = self._config.db.supabase_key
        
        if url and key and not url.startswith("${"):
            try:
                self.supabase = create_client(url, key)
                logger.info("Supabase client initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
        else:
            logger.warning("Supabase Config missing/unresolved. DB is operating in mock/fallback mode.")

    @classmethod
    def get_instance(cls, config: PsycheConfig | None = None) -> "PsycheDBClient":
        if cls._instance is None:
            cls._instance = cls(config)
        return cls._instance

    def save_listener_state(self, user_id: str, state_vector: BaseModel, signals: BaseModel) -> bool:
        """Persist a parsed ListenerStateVector to the DB."""
        if not self.supabase:
            return False
            
        try:
            data = {
                "user_id": user_id,
                "valence": state_vector.valence, # type: ignore
                "arousal": state_vector.arousal, # type: ignore
                "focus": state_vector.focus, # type: ignore
                "social_mode": state_vector.social_mode, # type: ignore
                "confidence": state_vector.confidence, # type: ignore
                "inference_method": getattr(state_vector, "method", "unknown"),
                "raw_signals": signals.model_dump()
            }
            
            response = self.supabase.table("listener_states").insert(data).execute()
            return len(response.data) > 0
        except Exception as e:
            logger.error(f"Error persisting listener state: {e}")
            return False
            
    def update_sonic_genome(self, user_id: str, delta: Dict[str, float]) -> bool:
        """Apply radar deltas directly to the user's base genome in PostgreSQL."""
        if not self.supabase:
            return False
            
        try:
            # We would typically do an RPC call here using Supabase to prevent read/write racing,
            # but for basic testing we can fetch and push.
            res = self.supabase.table("psyche_users").select("sonic_genome").eq("id", user_id).execute()
            if not res.data:
                return False
                
            genome = res.data[0].get("sonic_genome", {})
            for axis, change in delta.items():
                current = genome.get(axis, 0.5)
                genome[axis] = max(0.0, min(1.0, current + change))
                
            self.supabase.table("psyche_users").update({"sonic_genome": genome}).eq("id", user_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error updating sonic genome: {e}")
            return False
