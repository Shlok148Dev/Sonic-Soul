"""
Fairness RL Gymnasium Environment — For PPO training.

Action space: select from candidate embedding pool
Observation space: user embedding + candidate summary statistics
Reward: α·engagement + β·artist_diversity + γ·geographic_spread
"""

import logging
from typing import Any, Dict, Optional

import numpy as np

logger = logging.getLogger(__name__)

try:
    import gymnasium as gym
    from gymnasium import spaces
except ImportError:
    gym = None  # type: ignore


class FairnessRecommenderEnv:
    """
    Gymnasium environment for training the Fairness-Aware RL Recommender.

    State: concatenation of [user_embedding, candidate_pool_stats, fairness_stats]
    Action: index into candidate pool
    Reward: weighted sum of engagement + diversity + geographic spread
    """

    def __init__(
        self,
        embedding_dim: int = 40,
        n_candidates: int = 100,
        reward_alpha: float = 0.7,
        reward_beta: float = 0.2,
        reward_gamma: float = 0.1,
    ):
        self.embedding_dim = embedding_dim
        self.n_candidates = n_candidates
        self.reward_alpha = reward_alpha
        self.reward_beta = reward_beta
        self.reward_gamma = reward_gamma

        # State dimensions
        self.obs_dim = embedding_dim * 2 + 3  # user + candidate_mean + [gini, geo_spread, episode_step]

        # Track artists selected this episode for fairness calculation
        self.selected_artists: list = []
        self.episode_step = 0
        self.max_steps = 10  # recommend 10 tracks per episode

        # Placeholder data — replaced with real data during training
        self.user_embedding = np.zeros(embedding_dim, dtype=np.float32)
        self.candidate_embeddings = np.random.randn(n_candidates, embedding_dim).astype(np.float32)
        self.candidate_artists = [f"artist_{i % 20}" for i in range(n_candidates)]
        self.candidate_countries = [
            ["US", "UK", "SE", "JP", "BR", "NG", "KR", "IN", "DE", "FR"][i % 10]
            for i in range(n_candidates)
        ]

    @property
    def observation_space(self):
        if gym is None:
            return None
        return spaces.Box(low=-np.inf, high=np.inf, shape=(self.obs_dim,), dtype=np.float32)

    @property
    def action_space(self):
        if gym is None:
            return None
        return spaces.Discrete(self.n_candidates)

    def reset(self, seed=None) -> np.ndarray:
        """Reset environment for new episode."""
        self.selected_artists = []
        self.episode_step = 0
        # Generate new user embedding
        if seed is not None:
            np.random.seed(seed)
        self.user_embedding = np.random.randn(self.embedding_dim).astype(np.float32)
        return self._get_obs()

    def step(self, action: int):
        """Take an action (select a track) and return obs, reward, done, info."""
        self.episode_step += 1
        artist = self.candidate_artists[action]
        country = self.candidate_countries[action]
        self.selected_artists.append(artist)

        # Engagement reward: cosine similarity between user and selected track
        track_emb = self.candidate_embeddings[action]
        engagement = float(np.dot(self.user_embedding, track_emb) / (
            np.linalg.norm(self.user_embedding) * np.linalg.norm(track_emb) + 1e-8
        ))
        engagement = max(0, engagement)  # clip negative

        # Diversity reward: 1 - Gini of artist selection counts
        from collections import Counter
        counts = Counter(self.selected_artists)
        gini = self._gini(list(counts.values()))
        diversity = 1.0 - gini

        # Geographic spread: unique countries / total selections
        unique_countries = len(set(
            self.candidate_countries[i]
            for i, a in enumerate(self.candidate_artists)
            if a in self.selected_artists
        ))
        geo_spread = unique_countries / max(1, self.episode_step)

        # Combined reward
        reward = (
            self.reward_alpha * engagement
            + self.reward_beta * diversity
            + self.reward_gamma * geo_spread
        )

        done = self.episode_step >= self.max_steps
        info = {
            "engagement": engagement,
            "diversity": diversity,
            "geo_spread": geo_spread,
            "gini": gini,
        }

        return self._get_obs(), float(reward), done, info

    def _get_obs(self) -> np.ndarray:
        """Build observation vector."""
        candidate_mean = np.mean(self.candidate_embeddings, axis=0)
        from collections import Counter
        counts = Counter(self.selected_artists)
        gini = self._gini(list(counts.values())) if counts else 0.0
        unique_countries = len(set(
            self.candidate_countries[i]
            for i, a in enumerate(self.candidate_artists)
            if a in self.selected_artists
        )) if self.selected_artists else 0
        geo_spread = unique_countries / max(1, self.episode_step) if self.episode_step > 0 else 0
        stats = np.array([gini, geo_spread, self.episode_step / self.max_steps], dtype=np.float32)
        obs = np.concatenate([self.user_embedding, candidate_mean, stats])
        return obs

    @staticmethod
    def _gini(values: list) -> float:
        """Compute Gini coefficient."""
        if not values or sum(values) == 0:
            return 0.0
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        cumsum = np.cumsum(sorted_vals)
        return float(
            (2.0 * sum((i + 1) * v for i, v in enumerate(sorted_vals)) / (n * cumsum[-1]))
            - (n + 1) / n
        )
