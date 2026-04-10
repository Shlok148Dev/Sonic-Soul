"""
Rumination Guard — Addition 12.

Detects sustained negative valence patterns and intervenes
with gentle mood-lifting recommendations (opt-in only).
"""

import logging
from typing import Any, Dict, List

from psyche.agents.base import BasePsycheAgent
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class RuminationGuard(BasePsycheAgent):
    """Protects against sustained negative listening patterns."""

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "rumination_guard"

    async def infer(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Check if intervention is needed.
        Input: recent_valences (List[float]), opt_in (bool)
        """
        recent_valences: List[float] = kwargs.get("recent_valences", [])
        opt_in: bool = kwargs.get("opt_in", False)

        if not opt_in or len(recent_valences) < 3:
            return {"intervene": False, "reason": "not_applicable", "method": "check"}

        avg_valence = sum(recent_valences) / len(recent_valences)
        decline = recent_valences[-1] - recent_valences[0]

        intervene = (
            avg_valence < self._config.rumination_guard.arousal_floor
            or decline < self._config.rumination_guard.valence_decline_threshold
        )

        return {
            "intervene": intervene,
            "reason": "sustained_negative_valence" if intervene else "normal",
            "avg_valence": avg_valence,
            "method": "valence_monitoring",
        }

    def fallback(self, **kwargs: Any) -> Dict[str, Any]:
        return {"intervene": False, "reason": "fallback", "method": "fallback"}
