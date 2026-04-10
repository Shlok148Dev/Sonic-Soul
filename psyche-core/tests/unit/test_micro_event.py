"""Tests for the Micro-Event Attribution Engine."""

import pytest
import asyncio
from psyche.config import PsycheConfig
from psyche.agents.micro_event import MicroEventAttributionEngine

class TestMicroEventAttribution:
    def test_play_event_yields_normal_distribution(self):
        config = PsycheConfig()
        agent = MicroEventAttributionEngine(config)
        
        result = asyncio.run(agent.infer(track_id="123", event_type="play", event_timestamp_pct=1.0))
        assert result["track_id"] == "123"
        assert result["stem_attribution"]["vocals"] == 0.25
        assert result["stem_attribution"]["harmony"] == 0.25

    def test_hard_skip_yields_penalty(self):
        """A skip at 10% should penalize vocals and harmony heavily."""
        config = PsycheConfig()
        agent = MicroEventAttributionEngine(config)
        
        result = asyncio.run(agent.infer(track_id="123", event_type="skip", event_timestamp_pct=0.1))
        # Skip penalty = 1.0 - 0.1 = 0.9
        # harmony = 0.25 - 0.09 = 0.16
        # vocals = 0.25 - 0.135 = 0.115
        
        attr = result["stem_attribution"]
        assert attr["vocals"] < 0.25
        assert attr["harmony"] < 0.25
        assert result["micro_events"][0]["type"] == "skip"

    def test_fallback(self):
        config = PsycheConfig()
        agent = MicroEventAttributionEngine(config)
        result = agent.fallback(track_id="123")
        assert result["method"] == "fallback"
