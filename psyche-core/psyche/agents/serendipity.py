"""
Serendipity Discovery Agent — Gap 4.

Finds acoustically similar but contextually surprising tracks using
CLAP embeddings + FAISS similarity search with a novelty sweet spot.

Novelty sweet spot: similarity ∈ [0.35, 0.75] — not too familiar, not alien.
"""

import logging
from typing import Any, Dict, List

import numpy as np

from psyche.agents.base import BasePsycheAgent
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class SerendipityAgent(BasePsycheAgent):
    """Discovers new music in the novelty sweet spot."""

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "serendipity"

    async def infer(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Find serendipitous recommendations from FAISS/CLAP index.
        Input: user_clap_centroid (np.ndarray), history_ids (List[str]), n (int)
        Output: {track_ids, scores, serendipity_rate}
        """
        user_centroid = kwargs["user_clap_centroid"]
        history_ids = set(kwargs.get("history_ids", []))
        n = kwargs.get("n", 10)

        import faiss
        import json

        index = faiss.read_index(self._config.faiss.clap_index_path)
        with open(self._config.faiss.clap_id_map_path) as f:
            id_map = json.load(f)

        k = self._config.serendipity.k_candidates
        distances, indices = index.search(
            np.array([user_centroid], dtype=np.float32), k
        )

        min_sim = self._config.serendipity.novelty_sweet_spot[0]
        max_sim = self._config.serendipity.novelty_sweet_spot[1]

        candidates = []
        for dist, idx in zip(distances[0], indices[0]):
            sim = 1.0 / (1.0 + dist)
            track_id = id_map[str(idx)]
            if track_id not in history_ids and min_sim <= sim <= max_sim:
                candidates.append((track_id, sim))

        candidates.sort(key=lambda x: abs(x[1] - 0.55))  # Closest to sweet spot center
        selected = candidates[:n]

        serendipity_rate = len(selected) / max(1, n)

        return {
            "track_ids": [t[0] for t in selected],
            "scores": [t[1] for t in selected],
            "serendipity_rate": serendipity_rate,
            "method": "clap_novelty_search",
        }

    def fallback(self, **kwargs: Any) -> Dict[str, Any]:
        """Random selection fallback."""
        return {
            "track_ids": [],
            "scores": [],
            "serendipity_rate": 0.0,
            "method": "fallback_empty",
        }
