"""Unit tests for Pydantic data models."""

import pytest

from psyche.models.listener_state import ListenerStateVector, SessionSignals
from psyche.models.track import Track, RecommendedTrack, IntegrityScore
from psyche.models.sonic_genome import SonicGenome, StemPreference, MicroEvent
from psyche.models.context import SessionContext, ContextProfile


class TestListenerStateVector:
    def test_valid_creation(self):
        state = ListenerStateVector(
            valence=0.5, arousal=-0.3, focus=0.8,
            social_mode=0.2, confidence=0.9, method="test"
        )
        assert state.valence == 0.5
        assert state.method == "test"

    def test_out_of_range_valence_fails(self):
        with pytest.raises(Exception):
            ListenerStateVector(
                valence=2.0, arousal=0.0, focus=0.5,
                social_mode=0.2, confidence=0.5, method="test"
            )

    def test_frozen(self):
        state = ListenerStateVector(
            valence=0.0, arousal=0.0, focus=0.5,
            social_mode=0.2, confidence=0.5, method="test"
        )
        with pytest.raises(Exception):
            state.valence = 1.0


class TestSessionSignals:
    def test_defaults(self):
        signals = SessionSignals(time_of_day=12.0, day_of_week=3)
        assert signals.recent_skips == 0
        assert signals.stated_activity == "unspecified"


class TestTrack:
    def test_creation(self):
        track = Track(track_id="123", title="Test", artist="Test Artist", duration_seconds=180)
        assert track.track_id == "123"


class TestIntegrityScore:
    def test_passed(self):
        score = IntegrityScore(
            track_id="t1", ai_generated=0.1, toxic=0.05, spoofed=0.0, passed=True
        )
        assert score.passed is True
