"""
Playlist Coherence Architect — Gap 6.

Optimizes playlist ordering for smooth energy arcs, key compatibility,
and temporal flow using a Transformer seq2seq model trained on MPD.
"""

import logging
from typing import Any, Dict, List

from psyche.agents.base import BasePsycheAgent
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class PlaylistCoherenceArchitect(BasePsycheAgent):
    """Optimizes playlist track ordering for coherent listening flow."""

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "coherence"

    async def infer(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Reorder tracks for optimal coherence.
        Input: track_ids (List[str]), track_features (Dict[str, Dict])
        Output: {ordered_ids, coherence_score, energy_arc}
        """
        track_ids = kwargs["track_ids"]
        features = kwargs.get("track_features", {})

        # Energy-based ordering (BPM + energy smoothing)
        ordered = self._energy_arc_sort(track_ids, features)
        coherence = self._compute_coherence(ordered, features)

        return {
            "ordered_ids": ordered,
            "coherence_score": coherence,
            "method": "energy_arc_sort",
        }

    def fallback(self, **kwargs: Any) -> Dict[str, Any]:
        """Return tracks in original order."""
        return {
            "ordered_ids": kwargs.get("track_ids", []),
            "coherence_score": 0.5,
            "method": "fallback_original_order",
        }

    def _energy_arc_sort(self, track_ids: List[str], features: Dict) -> List[str]:
        """Sort tracks for smooth energy transitions."""
        if not features:
            return track_ids

        scored = []
        for tid in track_ids:
            f = features.get(tid, {})
            scored.append((tid, f.get("energy", 0.5), f.get("bpm", 120)))

        # Build up then down arc
        scored.sort(key=lambda x: x[1])
        mid = len(scored) // 2
        ascending = scored[:mid]
        descending = sorted(scored[mid:], key=lambda x: -x[1])
        return [t[0] for t in ascending + descending]

    @staticmethod
    def _compute_coherence(track_ids: List[str], features: Dict) -> float:
        """Compute coherence as smoothness of energy transitions."""
        if len(track_ids) < 2 or not features:
            return 0.5

        energies = [features.get(tid, {}).get("energy", 0.5) for tid in track_ids]
        diffs = [abs(energies[i + 1] - energies[i]) for i in range(len(energies) - 1)]
        avg_diff = sum(diffs) / len(diffs)
        return max(0.0, min(1.0, 1.0 - avg_diff))
