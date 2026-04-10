"""Tests for the Sonic Explainability Agent (SEA)."""

import pytest
from psyche.config import PsycheConfig
from psyche.agents.explainability import SonicExplainabilityAgent

class TestSEA:
    def test_fallback_generates_strings(self):
        config = PsycheConfig()
        agent = SonicExplainabilityAgent(config)
        
        res1 = agent.fallback(track_name="Neon Run", method="fairness_rl")
        assert "fresh dynamic" in res1["explanation"]
        
        res2 = agent.fallback(track_name="Neon Run", method="serendipity")
        assert "unexpected detour" in res2["explanation"]

    def test_prompt_generation_contextualizes_arousal(self):
        config = PsycheConfig()
        agent = SonicExplainabilityAgent(config)
        
        prompt_high = agent._build_prompt("Speed", "Runner", {"arousal": 0.8})
        assert "high energy" in prompt_high

        prompt_low = agent._build_prompt("Calm", "Walker", {"arousal": 0.2})
        assert "calm focus" in prompt_low
