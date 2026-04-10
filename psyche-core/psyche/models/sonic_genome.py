"""
Sonic Genome — Per-user representation of acoustic preferences.

Built from Micro-Event Attribution Engine analysis of which acoustic
sub-components drive a user's engagement (skips, replays, saves).
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class MicroEvent(BaseModel):
    """A specific acoustic micro-event that drives user engagement."""

    model_config = ConfigDict(frozen=True)

    event_type: str = Field(
        ...,
        description="Type: 'bridge_tension' | 'bass_drop' | 'key_change' | 'bpm_shift' | 'vocal_entry' | 'stem_solo'",
    )
    engagement_score: float = Field(
        ..., ge=0.0, le=1.0, description="How much this event drives engagement"
    )
    frequency: int = Field(
        ..., description="How many times this event type has been encountered"
    )
    avg_timestamp_pct: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Average position in track where this event occurs (0=start, 1=end)",
    )


class StemPreference(BaseModel):
    """User preference for individual audio stems."""

    model_config = ConfigDict(frozen=True)

    vocals_engagement: float = Field(
        ..., ge=0.0, le=1.0, description="Engagement rate with vocal-forward moments"
    )
    bass_engagement: float = Field(
        ..., ge=0.0, le=1.0, description="Engagement rate with bass-forward moments"
    )
    drums_engagement: float = Field(
        ..., ge=0.0, le=1.0, description="Engagement rate with drum-forward moments"
    )
    harmony_engagement: float = Field(
        ..., ge=0.0, le=1.0, description="Engagement rate with harmony/melody moments"
    )


class SonicGenome(BaseModel):
    """
    The complete per-user Sonic Genome.
    Built from Micro-Event Attribution Engine + CLAP/MERT embeddings.
    """

    model_config = ConfigDict(frozen=True)

    user_id: str = Field(..., description="User identifier")
    top_micro_events: List[MicroEvent] = Field(
        ..., description="Top 10 micro-events by engagement score"
    )
    stem_preference: StemPreference = Field(
        ..., description="Per-stem engagement rates"
    )
    clap_centroid: Optional[List[float]] = Field(
        default=None, description="Average CLAP embedding (512-dim) of engaged tracks"
    )
    mert_centroid: Optional[List[float]] = Field(
        default=None, description="Average MERT embedding (768-dim) of engaged tracks"
    )
    taste_vector: Dict[str, float] = Field(
        default_factory=dict,
        description="5-axis radar: harmonic_complexity, rhythmic_drive, emotional_depth, discovery_hunger, social_mode",
    )
    total_tracks_analyzed: int = Field(
        default=0, description="Number of tracks contributing to this genome"
    )
