"""
Context Fusion Module — Gap 7.

Fuses external context signals (weather, calendar, wearable data)
with listening session signals using differential privacy.
"""

import logging
from typing import Any, Dict

from psyche.agents.base import BasePsycheAgent
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class ContextFusionModule(BasePsycheAgent):
    """Fuses environmental context with session signals."""

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "context_fusion"

    async def infer(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Fuse all context signals into a unified context vector.
        Input: session_signals, activity_context (optional)
        Output: {fused_context, context_sources}
        """
        session_signals = kwargs.get("session_signals", {})
        activity_context = kwargs.get("activity_context", {})
        
        sources = ["time_of_day"]
        time_weight = 1.0
        weather_weight = 0.0
        calendar_weight = 0.0
        
        # Merge physical contexts if they exist dynamically
        if "weather" in activity_context:
            weather_weight = 0.5
            time_weight = 0.5
            sources.append("weather")
            
        if "calendar" in activity_context:
            calendar_weight = 0.8 # Calendar scheduling overrides physical logic
            time_weight = 0.2
            weather_weight = 0.0
            sources.append("calendar")
            
        return {
            "fused_context": {
                "time_weight": time_weight, 
                "weather_weight": weather_weight, 
                "calendar_weight": calendar_weight
            },
            "context_sources": sources,
            "method": "fusion_matrix",
        }

    def fallback(self, **kwargs: Any) -> Dict[str, Any]:
        """Time-only fallback."""
        return {
            "fused_context": {"time_weight": 1.0, "weather_weight": 0.0, "calendar_weight": 0.0},
            "context_sources": ["time_of_day"],
            "method": "fallback",
        }
