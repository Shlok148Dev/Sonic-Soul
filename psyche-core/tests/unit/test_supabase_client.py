"""Unit tests for the Supabase Client wrapper."""

import pytest
from pydantic import BaseModel
from psyche.config import PsycheConfig
from psyche.db.supabase_client import PsycheDBClient
from psyche.models.listener_state import ListenerStateVector, SessionSignals

class TestPsycheDBClient:
    """Test functionality of PsycheDBClient connection pools."""

    def test_mock_fallback_no_credentials(self):
        """Client should fallback gracefully when .env credentials are missing."""
        config = PsycheConfig()
        # Force missing credentials
        config.db.supabase_url = ""
        config.db.supabase_key = ""
        
        client = PsycheDBClient(config=config)
        assert client.supabase is None
        
        # Test safe fallback mapping
        state = ListenerStateVector(
            valence=0.5, arousal=0.5, focus=0.5, social_mode=0.5, confidence=0.5, method="test_mock"
        )
        signals = SessionSignals(time_of_day=12.0, day_of_week=3)
        
        # Operations should silently return False lacking a db connection
        assert client.save_listener_state("test-uuid", state, signals) is False
        assert client.update_sonic_genome("test-uuid", {"rhythmic_drive": 0.1}) is False
