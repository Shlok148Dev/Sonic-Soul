"""Unit tests for evaluation metrics."""

import numpy as np
import pytest

from psyche.utils.metrics import (
    serendipity_rate,
    gini_coefficient,
    coherence_score,
    precision_at_k,
    recall_at_k,
)


class TestSerendipityRate:
    def test_all_novel(self):
        recs = ["a", "b", "c"]
        history = {"d", "e", "f"}
        assert serendipity_rate(recs, history) == 1.0

    def test_all_known(self):
        recs = ["a", "b", "c"]
        history = {"a", "b", "c"}
        assert serendipity_rate(recs, history) == 0.0

    def test_partial(self):
        recs = ["a", "b", "c", "d"]
        history = {"a", "b"}
        assert serendipity_rate(recs, history) == 0.5

    def test_empty_recs(self):
        assert serendipity_rate([], {"a"}) == 0.0


class TestCoherenceScore:
    def test_identical_embeddings(self):
        embs = [np.array([1.0, 0.0]), np.array([1.0, 0.0])]
        assert coherence_score(embs) == pytest.approx(1.0)

    def test_single_embedding(self):
        assert coherence_score([np.array([1.0, 0.0])]) == 1.0


class TestPrecisionAtK:
    def test_perfect_precision(self):
        recs = ["a", "b", "c"]
        relevant = {"a", "b", "c"}
        assert precision_at_k(recs, relevant, k=3) == 1.0

    def test_zero_precision(self):
        recs = ["x", "y", "z"]
        relevant = {"a", "b", "c"}
        assert precision_at_k(recs, relevant, k=3) == 0.0


class TestRecallAtK:
    def test_perfect_recall(self):
        recs = ["a", "b", "c"]
        relevant = {"a", "b"}
        assert recall_at_k(recs, relevant, k=3) == 1.0

    def test_zero_recall(self):
        recs = ["x", "y", "z"]
        relevant = {"a", "b"}
        assert recall_at_k(recs, relevant, k=3) == 0.0
