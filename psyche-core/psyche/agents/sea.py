"""
Sonic Explainability Agent (SEA) — Gap 10.

Generates natural language explanations for every recommendation using
RAG pipeline: FAISS audio features → Ollama LLM explanation generation.

Every recommendation gets: "Why this track?" in musical language that
references specific audio features, artist context, and Sonic Genome patterns.
"""

import logging
from typing import Any, Dict

from psyche.agents.base import BasePsycheAgent
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class SonicExplainabilityAgent(BasePsycheAgent):
    """SEA — explains every recommendation in musical language."""

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "sea"

    async def infer(self, **kwargs: Any) -> Dict[str, str]:
        """
        Generate explanation for a recommended track.
        Input: track_id, track_features, user_genome, listener_state, agent_source
        Output: {"explanation": "...", "method": "llm_rag"}
        """
        import httpx

        track_id = kwargs["track_id"]
        track_features = kwargs.get("track_features", {})
        user_genome = kwargs.get("user_genome", {})
        agent_source = kwargs.get("agent_source", "unknown")

        prompt = self._build_explanation_prompt(
            track_id, track_features, user_genome, agent_source
        )

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._config.esie.ollama_host}/api/generate",
                json={
                    "model": self._config.esie.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=15.0,
            )
            response.raise_for_status()
            explanation = response.json()["response"]

        return {"explanation": explanation.strip(), "method": "llm_rag"}

    def fallback(self, **kwargs: Any) -> Dict[str, str]:
        """Template-based explanation fallback."""
        agent_source = kwargs.get("agent_source", "unknown")
        templates = {
            "fairness_rl": "Recommended for balanced discovery — this artist deserves your attention.",
            "serendipity": "Something new for your ears — outside your usual patterns but acoustically aligned.",
            "coherence": "Chosen to maintain the energy flow of your current session.",
            "clap_similarity": "Acoustically similar to tracks you've engaged with deeply.",
        }
        explanation = templates.get(
            agent_source,
            "Selected by PSYCHE to match your current listening state.",
        )
        return {"explanation": explanation, "method": "template_fallback"}

    def _build_explanation_prompt(
        self, track_id: str, features: Dict, genome: Dict, source: str
    ) -> str:
        """Build the RAG prompt for explanation generation."""
        return f"""You are SEA, the Sonic Explainability Agent. Generate a 1-2 sentence musical explanation
for why this track was recommended.

Track: {track_id}
Audio features: {features}
User Sonic Genome highlights: {genome}
Source agent: {source}

Rules:
- Reference specific audio characteristics (tempo, key, energy, harmony)
- Mention the user's engagement patterns if relevant
- Use musical language, not generic recommendations language
- Keep under 50 words
- Never say "you might like" or "we think you'll enjoy"

Output ONLY the explanation text, nothing else."""
