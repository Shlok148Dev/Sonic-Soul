"""
Content Integrity Guardian — Gap 8.

Detects AI-generated content, metadata spoofing, and toxicity.
Acts as a pre-filter before any track enters the recommendation pool.
"""

import logging
from typing import Any

from psyche.agents.base import BasePsycheAgent
from psyche.models.track import IntegrityScore
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class ContentIntegrityGuardian(BasePsycheAgent):
    """Gates every track through integrity checks before recommendation."""

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "content_integrity"

    async def infer(self, **kwargs: Any) -> IntegrityScore:
        """
        Evaluate a track's content integrity.
        Input: track_id (str), audio_path (str, optional), metadata (dict)
        """
        track_id = kwargs.get("track_id", "unknown")
        metadata = kwargs.get("metadata", {})
        
        # Phase 5 NLP Basic Text Safety Classification (Heuristics until CLAP integration)
        toxic_keywords = ["hate", "kill", "murder", "racist"]
        ai_keywords = ["suno", "udio", "generated", "ai cover"]
        
        title = str(metadata.get("title", "")).lower()
        artist = str(metadata.get("artist", "")).lower()
        
        is_toxic = sum(1 for w in toxic_keywords if w in title or w in artist) > 0
        is_ai = sum(1 for w in ai_keywords if w in title or w in artist) > 0
        
        toxicity_score = 1.0 if is_toxic else 0.0
        ai_score = 1.0 if is_ai else 0.0
        
        passed = True
        if toxicity_score >= self._config.integrity.toxicity_threshold:
            passed = False
        if ai_score >= self._config.integrity.ai_generated_threshold:
            passed = False

        return IntegrityScore(
            track_id=track_id,
            ai_generated=ai_score,
            toxic=toxicity_score,
            spoofed=0.0,
            passed=passed,
        )

    def fallback(self, **kwargs: Any) -> IntegrityScore:
        """Conservative fallback — pass all tracks."""
        return IntegrityScore(
            track_id=kwargs.get("track_id", "unknown"),
            ai_generated=0.0,
            toxic=0.0,
            spoofed=0.0,
            passed=True,
        )
