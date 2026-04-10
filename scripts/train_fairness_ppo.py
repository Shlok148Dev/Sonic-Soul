#!/usr/bin/env python3
"""
Train the PSYCHE Fairness-Aware RL Agent.

Executes a PPO training run on the FairnessRecommenderEnv Gymnasium
environment and exports the model to the primary binary data location
for dynamic loading by the orchestrator.
"""

import logging
import os
import argparse
from pathlib import Path

# Provide mock testing defaults in case we run in constrained setups
try:
    from stable_baselines3 import PPO
    from stable_baselines3.common.env_checker import check_env
except ImportError:
    PPO = None

from psyche.config import PsycheConfig
from psyche.environments.fairness_env import FairnessRecommenderEnv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Train the Fairness RL Agent")
    parser.add_argument("--timesteps", type=int, default=50000, help="Number of training timesteps")
    args = parser.parse_args()

    if PPO is None:
        logger.error("Skipping training: stable_baselines3 is not installed or configured correctly.")
        return

    logger.info("Initializing configuration and Gymnasium Environment...")
    config = PsycheConfig.from_yaml()
    
    env = FairnessRecommenderEnv(
        embedding_dim=40,
        n_candidates=100,
        reward_alpha=config.fairness.reward_alpha,
        reward_beta=config.fairness.reward_beta,
        reward_gamma=config.fairness.reward_gamma,
    )
    
    # Optional sanity check prior to training mapping
    check_env(env)
    
    logger.info("Starting PPO Training architecture...")
    model = PPO(
        policy=config.fairness.ppo_policy,
        env=env,
        verbose=1,
        policy_kwargs={"net_arch": config.fairness.ppo_net_arch}
    )
    
    model.learn(total_timesteps=args.timesteps, progress_bar=True)
    
    output_path = Path("data/models/fairness_ppo.zip")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    model.save(str(output_path))
    logger.info(f"Model successfully saved to {output_path}")


if __name__ == "__main__":
    main()
