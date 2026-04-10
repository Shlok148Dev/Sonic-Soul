"""Unit tests for Cold Start agent."""

import pytest

from psyche.agents.cold_start import ColdStartPsychographicAgent


class TestColdStart:
    """Test Cold Start Psychographic Agent."""

    def test_fallback_returns_valid_dict(self):
        """Fallback must always return a dictionary with expected keys."""
        agent = ColdStartPsychographicAgent()
        result = agent.fallback(turn=1)
        
        assert isinstance(result, dict)
        assert "next_question" in result
        assert "radar_delta" in result
        assert "agent_response" in result
        assert "interview_complete" in result
        assert not result["interview_complete"]

    def test_fallback_completes_at_turn_6(self):
        """Interview should be marked complete if turn > 5."""
        agent = ColdStartPsychographicAgent()
        result = agent.fallback(turn=6)
        
        assert result["interview_complete"] is True
        assert result["next_question"] is None
        assert isinstance(result["radar_delta"], dict)

    def test_fallback_different_turns_yield_different_responses(self):
        """Different turns should yield different dummy delta updates."""
        agent = ColdStartPsychographicAgent()
        result_t1 = agent.fallback(turn=1)
        result_t3 = agent.fallback(turn=3)
        
        assert result_t1["radar_delta"] != result_t3["radar_delta"]
        assert result_t1["next_question"] != result_t3["next_question"]
