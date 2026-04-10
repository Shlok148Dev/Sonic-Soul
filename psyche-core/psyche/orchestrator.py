"""
PSYCHE Meta-Orchestrator — The central brain.

Blends outputs from all 12 agents based on listener state,
dynamically adjusting weights for fairness, serendipity,
coherence, and similarity. Falls back to pure rules if LLM unavailable.
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

from psyche.config import PsycheConfig
from psyche.models.listener_state import ListenerStateVector

logger = logging.getLogger(__name__)


class PsycheMetaOrchestrator:
    """
    Central orchestration layer. Runs all agents in parallel,
    blends results based on listener state, returns final ranked list.
    """

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()
        self._agents: Dict[str, Any] = {}

    def register_agent(self, agent: Any) -> None:
        """Register an agent with the orchestrator."""
        self._agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")

    async def recommend(
        self,
        listener_state: ListenerStateVector,
        n: int = 10,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        """
        Run all agents in parallel, blend results, return ranked tracks.
        """
        start = time.perf_counter()

        # Run all agents concurrently
        agent_tasks = {
            name: agent.run(**kwargs)
            for name, agent in self._agents.items()
        }

        results = {}
        for name, task in agent_tasks.items():
            try:
                results[name] = await task
            except Exception as e:
                logger.error(f"Agent {name} failed completely: {e}")
                results[name] = None

        # Compute dynamic weights based on listener state
        weights = self._compute_weights(listener_state)

        # Blend agent outputs (simplified — full LLM blend in Week 7)
        blended = self._blend_results(results, weights, n)

        elapsed_ms = (time.perf_counter() - start) * 1000

        return {
            "recommendations": blended,
            "agent_weights": weights,
            "agent_results": {k: v for k, v in results.items() if v is not None},
            "total_latency_ms": elapsed_ms,
            "listener_state": listener_state.model_dump(),
        }

    def _compute_weights(self, state: ListenerStateVector) -> Dict[str, float]:
        """Compute agent weights based on listener state."""
        base = dict(self._config.orchestrator.base_weights)

        # High arousal → boost coherence (workouts need flow)
        if state.arousal > 0.5:
            base["coherence"] *= self._config.orchestrator.high_arousal_coherence_boost

        # High focus → penalize serendipity (don't distract)
        if state.focus > 0.7:
            base["serendipity"] *= self._config.orchestrator.high_focus_serendipity_penalty

        # Low confidence → boost similarity (play it safe)
        if state.confidence < 0.4:
            base["clap_similarity"] *= self._config.orchestrator.low_confidence_similarity_boost

        # Normalize
        total = sum(base.values())
        return {k: v / total for k, v in base.items()}

    def _blend_results(
        self, results: Dict, weights: Dict, n: int
    ) -> List[Dict[str, Any]]:
        """Blend agent outputs into a final ranked list."""
        # Collect all candidate track IDs with scores
        scored: Dict[str, float] = {}

        # Extract fairness Gini coefficient for Meta-Balancing
        fairness_output = results.get("fairness_rl")
        if fairness_output is not None and fairness_output.get("result"):
            gini = fairness_output["result"].get("gini_coefficient", 0.0)
            if gini > 0.4:
                logger.debug(f"High artist Gini ({gini:.2f}) detected. Orchestrator suppressing Popularity weights +50%.")
                if "popularity" in weights:
                    weights["popularity"] *= 0.5
                if "fairness_rl" in weights:
                    weights["fairness_rl"] *= 1.5

        for agent_name, result in results.items():
            if result is None or result.get("result") is None:
                continue

            agent_out = result["result"]
            weight = weights.get(agent_name, 0.1)

            track_ids = agent_out.get("track_ids", [])
            scores = agent_out.get("scores", [1.0] * len(track_ids))

            for tid, score in zip(track_ids, scores):
                scored[tid] = scored.get(tid, 0.0) + weight * score

        # Sort by blended score, take top n
        ranked = sorted(scored.items(), key=lambda x: -x[1])[:n]

        return [
            {"track_id": tid, "blended_score": score}
            for tid, score in ranked
        ]

    def health(self) -> Dict[str, Any]:
        """Return health status of all registered agents."""
        statuses = {}
        for name, agent in self._agents.items():
            try:
                statuses[name] = agent.health_check().model_dump()
            except Exception as e:
                statuses[name] = {"status": "failed", "error": str(e)}
        return {"agents": statuses, "total_registered": len(self._agents)}
