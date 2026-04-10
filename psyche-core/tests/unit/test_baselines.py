"""Unit tests for baseline recommenders."""

import numpy as np
import pytest

from psyche.baselines import (
    RandomRecommender,
    PopularityRecommender,
    MFCCRecommender,
)


class TestRandomRecommender:
    def test_returns_correct_count(self):
        track_ids = [f"track_{i}" for i in range(100)]
        rec = RandomRecommender(track_ids)
        result = rec.recommend("user1", n=10)
        assert len(result) == 10

    def test_no_duplicates(self):
        track_ids = [f"track_{i}" for i in range(100)]
        rec = RandomRecommender(track_ids)
        result = rec.recommend("user1", n=10)
        assert len(set(result)) == 10

    def test_handles_small_catalog(self):
        track_ids = [f"track_{i}" for i in range(5)]
        rec = RandomRecommender(track_ids)
        result = rec.recommend("user1", n=10)
        assert len(result) == 5


class TestPopularityRecommender:
    def test_returns_correct_count(self):
        track_ids = [f"track_{i}" for i in range(100)]
        scores = np.random.rand(100)
        rec = PopularityRecommender(track_ids, scores)
        result = rec.recommend("user1", n=10)
        assert len(result) == 10


class TestMFCCRecommender:
    def test_returns_similar_tracks(self):
        np.random.seed(42)
        n = 50
        track_ids = [f"track_{i}" for i in range(n)]
        features = np.random.randn(n, 40).astype(np.float32)
        rec = MFCCRecommender(track_ids, features)
        result = rec.recommend("user1", n=5, seed_track_idx=0)
        assert len(result) == 5
        assert "track_0" not in result  # seed excluded

    def test_does_not_include_seed(self):
        np.random.seed(42)
        n = 20
        track_ids = [f"track_{i}" for i in range(n)]
        features = np.random.randn(n, 40).astype(np.float32)
        rec = MFCCRecommender(track_ids, features)
        result = rec.recommend("user1", n=10, seed_track_idx=5)
        assert "track_5" not in result
