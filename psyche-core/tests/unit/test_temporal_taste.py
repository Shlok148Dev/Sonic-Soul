"""Tests for the Temporal Taste Agent."""

import pytest
import asyncio
from psyche.config import PsycheConfig
from psyche.agents.temporal_taste import TemporalTasteModel

class TestTemporalTaste:
    def test_long_history_yields_high_drift(self):
        config = PsycheConfig()
        agent = TemporalTasteModel(config)
        
        history = [{"id": "t1"} for _ in range(30)] # Size 30
        result = asyncio.run(agent.infer(user_id="u1", listening_history=history))
        
        # drift = min(30 * 0.02, 0.8) = 0.6
        assert result["taste_drift_rate"] == 0.6
        assert result["predicted_future"][0] > 0.5  # Positive shift

    def test_empty_history_yields_zero_drift(self):
        config = PsycheConfig()
        agent = TemporalTasteModel(config)
        
        result = asyncio.run(agent.infer(user_id="u1"))
        assert result["taste_drift_rate"] == 0.0
        assert result["predicted_future"][0] == 0.5

    def test_fallback(self):
        config = PsycheConfig()
        agent = TemporalTasteModel(config)
        result = agent.fallback()
        assert result["method"] == "fallback"
