"""Unit tests for the Fairness RL environment."""

import numpy as np
import pytest

from psyche.environments.fairness_env import FairnessRecommenderEnv


class TestFairnessEnv:
    def test_reset_returns_correct_shape(self):
        env = FairnessRecommenderEnv(embedding_dim=40, n_candidates=50)
        obs = env.reset(seed=42)
        assert obs.shape == (env.obs_dim,)

    def test_step_returns_reward(self):
        env = FairnessRecommenderEnv(embedding_dim=40, n_candidates=50)
        env.reset(seed=42)
        obs, reward, done, info = env.step(0)
        assert isinstance(reward, float)
        assert not done  # First step shouldn't be done

    def test_episode_ends_after_max_steps(self):
        env = FairnessRecommenderEnv(embedding_dim=40, n_candidates=50)
        env.reset(seed=42)
        for i in range(10):
            obs, reward, done, info = env.step(i)
        assert done  # Should be done after 10 steps

    def test_diversity_reward_penalizes_repetition(self):
        env = FairnessRecommenderEnv(embedding_dim=40, n_candidates=50)
        env.reset(seed=42)

        # Select same track repeatedly
        rewards_same = []
        for _ in range(5):
            _, r, _, info = env.step(0)
            rewards_same.append(info["diversity"])

        # Diversity should decrease with repetition
        assert rewards_same[-1] <= rewards_same[0]

    def test_info_contains_expected_keys(self):
        env = FairnessRecommenderEnv()
        env.reset(seed=42)
        _, _, _, info = env.step(0)
        assert "engagement" in info
        assert "diversity" in info
        assert "geo_spread" in info
        assert "gini" in info
