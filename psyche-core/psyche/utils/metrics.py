"""
PSYCHE Metrics — evaluation metrics for recommendation quality.

serendipity: fraction of recs the user hasn't heard before
diversity: Gini coefficient of artist play distribution
coherence: average cosine similarity of consecutive recs in CLAP space
"""

import numpy as np
from typing import Dict, List


def serendipity_rate(
    recommended_ids: List[str], history_ids: set[str]
) -> float:
    """Fraction of recommendations not in user's history."""
    if not recommended_ids:
        return 0.0
    novel = sum(1 for r in recommended_ids if r not in history_ids)
    return novel / len(recommended_ids)


def gini_coefficient(play_counts: Dict[str, int]) -> float:
    """
    Gini coefficient of artist play distribution.
    0 = perfectly equal, 1 = one artist gets all plays.
    """
    if not play_counts:
        return 0.0
    values = sorted(play_counts.values())
    n = len(values)
    cumsum = np.cumsum(values)
    return float(
        (2.0 * np.sum((np.arange(1, n + 1) * values)) / (n * cumsum[-1]))
        - (n + 1) / n
    )


def coherence_score(
    embeddings: List[np.ndarray],
) -> float:
    """
    Average cosine similarity between consecutive track embeddings.
    Higher = smoother transitions.
    """
    if len(embeddings) < 2:
        return 1.0

    similarities = []
    for i in range(len(embeddings) - 1):
        a, b = embeddings[i], embeddings[i + 1]
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a > 0 and norm_b > 0:
            sim = float(np.dot(a, b) / (norm_a * norm_b))
            similarities.append(sim)

    return float(np.mean(similarities)) if similarities else 0.0


def precision_at_k(
    recommended_ids: List[str], relevant_ids: set[str], k: int = 10
) -> float:
    """Precision@K — fraction of top-K recs that are relevant."""
    top_k = recommended_ids[:k]
    if not top_k:
        return 0.0
    hits = sum(1 for r in top_k if r in relevant_ids)
    return hits / len(top_k)


def recall_at_k(
    recommended_ids: List[str], relevant_ids: set[str], k: int = 10
) -> float:
    """Recall@K — fraction of relevant items found in top-K."""
    if not relevant_ids:
        return 0.0
    top_k = recommended_ids[:k]
    hits = sum(1 for r in top_k if r in relevant_ids)
    return hits / len(relevant_ids)
