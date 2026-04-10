"""
Track Models — All track-related Pydantic models.
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class Track(BaseModel):
    """A track in the PSYCHE catalog."""

    model_config = ConfigDict(frozen=True)

    track_id: str = Field(..., description="Unique track identifier")
    title: str = Field(..., description="Track title")
    artist: str = Field(..., description="Artist name")
    album: Optional[str] = Field(default=None, description="Album name")
    genre: Optional[str] = Field(default=None, description="Primary genre")
    duration_seconds: float = Field(..., description="Track duration in seconds")
    bpm: Optional[float] = Field(default=None, description="Beats per minute")
    key: Optional[str] = Field(default=None, description="Musical key (e.g. 'C major')")
    energy: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Energy level 0-1")
    valence: Optional[float] = Field(
        default=None, ge=-1.0, le=1.0, description="Emotional valence -1 to 1"
    )
    artist_country: Optional[str] = Field(default=None, description="Artist's country of origin")
    release_year: Optional[int] = Field(default=None, description="Release year")


class RecommendedTrack(BaseModel):
    """A track recommended by the PSYCHE system with full attribution."""

    model_config = ConfigDict(frozen=True)

    track_id: str = Field(..., description="Unique track identifier")
    title: str = Field(..., description="Track title")
    artist: str = Field(..., description="Artist name")
    explanation: str = Field(..., description="Natural language explanation from SEA")
    agent_source: str = Field(
        ..., description="Primary agent that surfaced this recommendation"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Recommendation confidence")
    latency_ms: float = Field(..., description="Inference latency for this recommendation")


class IntegrityScore(BaseModel):
    """Content Integrity Guardian output for a track."""

    model_config = ConfigDict(frozen=True)

    track_id: str = Field(..., description="Track identifier")
    ai_generated: float = Field(
        ..., ge=0.0, le=1.0, description="Probability of AI-generated content"
    )
    toxic: float = Field(..., ge=0.0, le=1.0, description="Toxicity score")
    spoofed: float = Field(
        ..., ge=0.0, le=1.0, description="Metadata spoofing probability"
    )
    passed: bool = Field(..., description="Whether the track passed all integrity checks")
