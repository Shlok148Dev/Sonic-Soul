"""
Baseline Recommenders B0-B4 — Week 1 Days 6-7.

B0: Random
B1: Popularity-weighted random
B2: MFCC cosine similarity
B3: CLAP cosine similarity
B4: ALS collaborative filtering (implicit)

These establish the floor that PSYCHE must exceed on every metric.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

logger = logging.getLogger(__name__)


class BaselineRecommender:
    """Base class for all baseline recommenders."""

    name: str = "base"

    def recommend(self, user_id: str, n: int = 10, **kwargs) -> List[str]:
        """Return a list of track IDs."""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"


class RandomRecommender(BaselineRecommender):
    """B0: Uniform random from catalog."""

    name = "B0_random"

    def __init__(self, track_ids: List[str]):
        self.track_ids = track_ids

    def recommend(self, user_id: str, n: int = 10, **kwargs) -> List[str]:
        return list(np.random.choice(
            self.track_ids, size=min(n, len(self.track_ids)), replace=False
        ))


class PopularityRecommender(BaselineRecommender):
    """B1: Popularity-weighted random sampling."""

    name = "B1_popularity"

    def __init__(self, track_ids: List[str], popularity_scores: np.ndarray):
        self.track_ids = track_ids
        self.probs = popularity_scores / popularity_scores.sum()

    def recommend(self, user_id: str, n: int = 10, **kwargs) -> List[str]:
        return list(np.random.choice(
            self.track_ids, size=min(n, len(self.track_ids)),
            replace=False, p=self.probs
        ))


class MFCCRecommender(BaselineRecommender):
    """B2: MFCC cosine similarity retrieval."""

    name = "B2_mfcc_similarity"

    def __init__(self, track_ids: List[str], mfcc_features: np.ndarray):
        self.track_ids = track_ids
        self.features = mfcc_features
        # Pre-normalize for cosine similarity
        norms = np.linalg.norm(mfcc_features, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.features_norm = mfcc_features / norms

    def recommend(
        self, user_id: str, n: int = 10, seed_track_idx: int = 0, **kwargs
    ) -> List[str]:
        """Find tracks most similar to seed track by MFCC cosine similarity."""
        query = self.features_norm[seed_track_idx:seed_track_idx + 1]
        sims = (self.features_norm @ query.T).flatten()
        # Exclude the seed track
        sims[seed_track_idx] = -1.0
        top_k = np.argsort(sims)[-n:][::-1]
        return [self.track_ids[i] for i in top_k]


class CLAPRecommender(BaselineRecommender):
    """B3: CLAP cosine similarity retrieval (requires CLAP embeddings)."""

    name = "B3_clap_similarity"

    def __init__(self, track_ids: List[str], clap_embeddings: np.ndarray):
        self.track_ids = track_ids
        self.embeddings = clap_embeddings
        norms = np.linalg.norm(clap_embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.embeddings_norm = clap_embeddings / norms

    def recommend(
        self, user_id: str, n: int = 10, seed_track_idx: int = 0, **kwargs
    ) -> List[str]:
        query = self.embeddings_norm[seed_track_idx:seed_track_idx + 1]
        sims = (self.embeddings_norm @ query.T).flatten()
        sims[seed_track_idx] = -1.0
        top_k = np.argsort(sims)[-n:][::-1]
        return [self.track_ids[i] for i in top_k]


class ALSRecommender(BaselineRecommender):
    """B4: Alternating Least Squares collaborative filtering."""

    name = "B4_als"

    def __init__(self, user_item_matrix=None):
        self.model = None
        self.user_item_matrix = user_item_matrix
        if user_item_matrix is not None:
            self._fit()

    def _fit(self):
        """Train ALS model on user-item interaction matrix."""
        try:
            from implicit.als import AlternatingLeastSquares
            import scipy.sparse as sp

            self.model = AlternatingLeastSquares(
                factors=64, iterations=20, regularization=0.1
            )
            sparse_matrix = sp.csr_matrix(self.user_item_matrix)
            self.model.fit(sparse_matrix)
            logger.info("ALS model trained successfully")
        except ImportError:
            logger.warning("implicit not installed — B4 baseline unavailable")

    def recommend(self, user_id: str, n: int = 10, user_idx: int = 0, **kwargs) -> List[str]:
        if self.model is None:
            return []
        import scipy.sparse as sp
        sparse = sp.csr_matrix(self.user_item_matrix)
        ids, scores = self.model.recommend(
            user_idx, sparse[user_idx], N=n, filter_already_liked_items=True
        )
        return [str(i) for i in ids]


def run_all_baselines(
    features_path: str = "data/features/librosa_features.parquet",
    output_path: str = "data/evaluation/baseline_results.json",
    n_test_users: int = 200,
) -> Dict:
    """Run all baseline recommenders and save results."""
    import pandas as pd
    from psyche.utils.metrics import serendipity_rate, gini_coefficient

    df = pd.read_parquet(features_path)
    track_ids = df["track_id"].tolist()

    # Create fake listening history (100 random tracks per user)
    np.random.seed(42)
    results = {}

    # B0: Random
    b0 = RandomRecommender(track_ids)
    b0_sers = []
    for _ in range(n_test_users):
        history = set(np.random.choice(track_ids, size=min(100, len(track_ids)), replace=False))
        recs = b0.recommend("test", n=10)
        b0_sers.append(serendipity_rate(recs, history))
    results["B0_random"] = {
        "serendipity_mean": float(np.mean(b0_sers)),
        "serendipity_std": float(np.std(b0_sers)),
    }

    # B1: Popularity
    energies = df.get("energy", pd.Series(np.ones(len(df)))).values
    b1 = PopularityRecommender(track_ids, energies)
    b1_sers = []
    for _ in range(n_test_users):
        history = set(np.random.choice(track_ids, size=min(100, len(track_ids)), replace=False))
        recs = b1.recommend("test", n=10)
        b1_sers.append(serendipity_rate(recs, history))
    results["B1_popularity"] = {
        "serendipity_mean": float(np.mean(b1_sers)),
        "serendipity_std": float(np.std(b1_sers)),
    }

    # B2: MFCC similarity
    mfcc_data = np.array(df["mfcc_mean"].tolist(), dtype=np.float32)
    b2 = MFCCRecommender(track_ids, mfcc_data)
    b2_recs = b2.recommend("test", n=10, seed_track_idx=0)
    results["B2_mfcc_similarity"] = {
        "sample_recs": b2_recs[:5],
        "method": "mfcc_cosine",
    }

    logger.info(f"Baseline results: {json.dumps(results, indent=2)}")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(results, indent=2))

    return results
