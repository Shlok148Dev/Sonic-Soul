"""Tests for Context Fusion Module."""

import pytest
import asyncio
from psyche.config import PsycheConfig
from psyche.agents.context_fusion import ContextFusionModule

class TestContextFusion:
    def test_weather_context_overrides_time(self):
        config = PsycheConfig()
        agent = ContextFusionModule(config)
        
        result = asyncio.run(agent.infer(activity_context={"weather": "rainy"}))
        assert "weather" in result["context_sources"]
        assert result["fused_context"]["weather_weight"] == 0.5
        assert result["fused_context"]["time_weight"] == 0.5

    def test_calendar_overrides_everything(self):
        config = PsycheConfig()
        agent = ContextFusionModule(config)
        
        result = asyncio.run(agent.infer(activity_context={"weather": "sunny", "calendar": "meeting"}))
        assert "calendar" in result["context_sources"]
        assert result["fused_context"]["calendar_weight"] == 0.8
        assert result["fused_context"]["weather_weight"] == 0.0

    def test_fallback(self):
        config = PsycheConfig()
        agent = ContextFusionModule(config)
        result = agent.fallback()
        assert result["method"] == "fallback"
        assert result["fused_context"]["time_weight"] == 1.0
