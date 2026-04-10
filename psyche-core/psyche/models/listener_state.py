"""
Listener State Models — The core emotional/cognitive state representation.

The ListenerStateVector is the primary output of ESIE and drives the
orchestrator's agent weighting decisions.
"""

from pydantic import BaseModel, ConfigDict, Field


class ListenerStateVector(BaseModel):
    """
    The listener's current emotional and cognitive state.
    Updated every 90 seconds by ESIE.
    """

    model_config = ConfigDict(frozen=True)

    valence: float = Field(
        ..., ge=-1.0, le=1.0, description="Emotional positivity. -1=very sad, +1=very happy"
    )
    arousal: float = Field(
        ..., ge=-1.0, le=1.0, description="Energy level. -1=very calm, +1=very energized"
    )
    focus: float = Field(
        ..., ge=0.0, le=1.0, description="Cognitive focus. 0=unfocused, 1=deep focus"
    )
    social_mode: float = Field(
        ..., ge=0.0, le=1.0, description="Social orientation. 0=solitary, 1=very social"
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="How confident ESIE is in this estimate"
    )
    method: str = Field(
        ...,
        description="Inference method: 'llm_inference' | 'signal_heuristic' | 'time_heuristic'",
    )


class SessionSignals(BaseModel):
    """
    Raw signals from the current listening session.
    Input to ESIE for state inference.
    """

    model_config = ConfigDict(frozen=True)

    time_of_day: float = Field(..., ge=0.0, le=24.0, description="Hour of day (0-24)")
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    recent_skips: int = Field(default=0, description="Skips in last 10 minutes")
    recent_replays: int = Field(default=0, description="Replays in last 10 minutes")
    session_length_minutes: float = Field(default=0.0, description="Session duration in minutes")
    stated_activity: str = Field(
        default="unspecified",
        description="Activity context: 'work'|'gym'|'sleep'|'commute'|'social'|'unspecified'",
    )
    recent_track_valences: list[float] = Field(
        default_factory=list, description="Valence values of last 5 tracks played"
    )
