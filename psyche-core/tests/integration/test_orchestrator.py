"""
Integration test for the full orchestrator pipeline.

Tests:
1. All 12 agents load and register
2. Health check returns for all agents
3. Orchestrator fallback mode works without external services
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "psyche-core"))


class TestOrchestratorIntegration:
    """Test the full orchestrator pipeline."""

    def test_all_agents_register(self):
        """All 12 agents should register without error."""
        from psyche.registry import build_orchestrator
        o = build_orchestrator()
        assert len(o._agents) == 12

    def test_health_check_all_agents(self):
        """Health check should return valid status for all agents."""
        from psyche.registry import build_orchestrator
        o = build_orchestrator()
        health = o.health()
        assert health["total_registered"] == 12
        for name, status in health["agents"].items():
            assert "status" in status, f"Agent {name} missing status"

    def test_agent_names_match_expected(self):
        """All expected agents should be present."""
        from psyche.registry import build_orchestrator
        o = build_orchestrator()
        expected = {
            "esie", "cold_start", "fairness_rl", "explainability", "serendipity",
            "coherence", "content_integrity", "micro_event",
            "temporal_taste", "context_fusion", "intent_classifier",
            "rumination_guard",
        }
        actual = set(o._agents.keys())
        assert actual == expected

    @pytest.mark.asyncio
    async def test_esie_fallback_through_orchestrator(self):
        """ESIE should produce valid state via fallback."""
        from psyche.agents.esie import EmotionalStateInferenceEngine
        esie = EmotionalStateInferenceEngine()
        result = await esie.run(time_of_day=14.0, day_of_week=2)
        assert result["agent"] == "esie"
        assert result["used_fallback"] is True  # No Ollama = fallback
        assert "valence" in str(result["result"])

    @pytest.mark.asyncio
    async def test_integrity_always_passes(self):
        """Content Integrity should pass all tracks (no model loaded yet)."""
        from psyche.agents.integrity import ContentIntegrityGuardian
        guard = ContentIntegrityGuardian()
        result = await guard.run(track_id="test_track")
        assert result["result"].passed is True
