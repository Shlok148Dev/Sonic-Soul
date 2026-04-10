"""Unit tests for ESIE agent."""

import pytest

from psyche.agents.esie import EmotionalStateInferenceEngine
from psyche.models.listener_state import ListenerStateVector


class TestESIE:
    """Test Emotional State Inference Engine."""

    def test_fallback_returns_valid_state(self):
        """Fallback must always return a valid ListenerStateVector."""
        esie = EmotionalStateInferenceEngine()
        result = esie.fallback(time_of_day=14.0, day_of_week=2)
        assert isinstance(result, ListenerStateVector)
        assert -1.0 <= result.valence <= 1.0
        assert -1.0 <= result.arousal <= 1.0
        assert 0.0 <= result.focus <= 1.0
        assert 0.0 <= result.social_mode <= 1.0

    def test_fallback_different_times_different_outputs(self):
        """Different times of day should produce different states."""
        esie = EmotionalStateInferenceEngine()
        morning = esie.fallback(time_of_day=8.0, day_of_week=1)
        night = esie.fallback(time_of_day=23.0, day_of_week=1)
        assert morning.arousal != night.arousal, "Morning and night should have different arousal"

    def test_fallback_social_activity(self):
        """Social activity should set high social_mode."""
        esie = EmotionalStateInferenceEngine()
        social = esie.fallback(time_of_day=20.0, day_of_week=5, stated_activity="social")
        work = esie.fallback(time_of_day=10.0, day_of_week=1, stated_activity="work")
        assert social.social_mode > work.social_mode
