"""
Context Models — Session, activity, and user context profiles.

These models power the Context Fusion Module (Gap 7) and
Context Profiles feature (Addition 03).
"""

from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class SessionContext(BaseModel):
    """Current session context signals for recommendation."""

    model_config = ConfigDict(frozen=True)

    time_of_day: float = Field(..., ge=0.0, le=24.0, description="Hour of day")
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    stated_activity: str = Field(
        default="unspecified",
        description="User-stated activity context",
    )
    recent_skips: int = Field(default=0, description="Skips in last 10 minutes")
    recent_replays: int = Field(default=0, description="Replays in last 10 minutes")
    recent_track_ids: List[str] = Field(
        default_factory=list, description="Recently played track IDs"
    )
    taste_lock: bool = Field(
        default=False, description="If true, this session has zero weight on taste profile"
    )


class ActivityContext(BaseModel):
    """Environmental and activity context from external sources."""

    model_config = ConfigDict(frozen=True)

    temperature_celsius: Optional[float] = Field(
        default=None, description="Current temperature from weather API"
    )
    weather_condition: Optional[str] = Field(
        default=None, description="Weather: 'clear' | 'cloudy' | 'rain' | 'snow'"
    )
    next_calendar_event_minutes: Optional[int] = Field(
        default=None, description="Minutes until next calendar event"
    )
    heart_rate_bpm: Optional[int] = Field(
        default=None, description="Heart rate from wearable webhook"
    )
    focus_score: Optional[float] = Field(
        default=None, ge=0.0, le=1.0, description="Focus score from productivity app webhook"
    )


class ContextProfile(BaseModel):
    """
    Named listening context profile (Addition 03).
    Each profile has its own ESIE parameters and taste weights.
    """

    model_config = ConfigDict(frozen=True)

    profile_name: str = Field(
        ..., description="Profile name: 'Work' | 'Sleep' | 'Gym' | 'Social' | 'Commute' | custom"
    )
    target_valence: float = Field(
        ..., ge=-1.0, le=1.0, description="Target emotional valence for this context"
    )
    target_arousal: float = Field(
        ..., ge=-1.0, le=1.0, description="Target energy level for this context"
    )
    serendipity_weight: float = Field(
        default=0.25, ge=0.0, le=1.0, description="Discovery vs familiarity balance"
    )
    coherence_weight: float = Field(
        default=0.25, ge=0.0, le=1.0, description="Smooth transitions importance"
    )
    taste_isolation: bool = Field(
        default=False,
        description="If true, listening in this profile doesn't affect other profiles",
    )
