"""
Intent Classifier — Detects listening intent mode.

Classifies: active, passive, background
Uses signals: skip rate, session length, time of day
"""

import logging
from typing import Any, Dict

from psyche.agents.base import BasePsycheAgent
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class IntentClassifier(BasePsycheAgent):
    """Classifies listening intent to adjust recommendation strategy."""

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "intent_classifier"

    async def infer(self, **kwargs: Any) -> Dict[str, Any]:
        """Classify listening intent from session signals."""
        time_of_day = kwargs.get("time_of_day", 12.0)
        recent_skips = kwargs.get("recent_skips", 0)
        session_minutes = kwargs.get("session_length_minutes", 0)

        # Fallbacks for passive schema limits
        passive_minutes = 30.0
        bg_ranges = [(6.0, 9.0), (22.0, 24.0)]

        # Rule-based classification
        if recent_skips == 0 and session_minutes > passive_minutes:
            intent = "passive"
        elif any(
            start <= time_of_day <= end or (start > end and (time_of_day >= start or time_of_day <= end))
            for start, end in bg_ranges
        ):
            intent = "background"
        else:
            intent = "active"

        return {"intent": intent, "confidence": 0.7, "method": "rule_based"}

    def fallback(self, **kwargs: Any) -> Dict[str, Any]:
        return {"intent": "active", "confidence": 0.3, "method": "fallback"}
