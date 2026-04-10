"""
Sonic Explainability Agent (SEA) — Gap 6.

Translates high-dimensional vector math and recommender decisions into 
human-readable narratives using Local LLMs.
"""

import logging
import json
from typing import Any, Dict

from psyche.agents.base import BasePsycheAgent
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class SonicExplainabilityAgent(BasePsycheAgent):
    """
    Explains the 'why' behind a recommendation.
    Generates short, punchy explanations contextualized to the listener's state.
    """

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "explainability"

    async def infer(self, **kwargs: Any) -> Dict[str, str]:
        """
        Generate explanation for a track recommendation.
        Input: track_metadata (dict), listener_state (dict), agent_weights (dict)
        Output: {"explanation": "short narrative string"}
        """
        import httpx

        track_name = kwargs.get("track_name", "this track")
        artist = kwargs.get("artist", "this artist")
        state = kwargs.get("listener_state", {})
        
        prompt = self._build_prompt(track_name, artist, state)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._config.esie.ollama_host}/api/generate",
                json={
                    "model": self._config.explainability.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=25.0,
            )
            response.raise_for_status()
            explanation = response.json()["response"]

        return {"explanation": explanation.strip()}

    def fallback(self, **kwargs: Any) -> Dict[str, str]:
        """Procedural template fallback if the LLM is offline."""
        track_name = kwargs.get("track_name", "This track")
        method = kwargs.get("method", "discovery")
        
        if "fairness" in method:
            return {"explanation": f"{track_name} brings a fresh dynamic to your usual rotation."}
        elif "serendipity" in method:
            return {"explanation": "A slightly unexpected detour that aligns perfectly with your sonic identity."}
        return {"explanation": "Because it matches the frequency of your current listening session."}

    def _build_prompt(self, track_name: str, artist: str, state: Dict[str, Any]) -> str:
        """Construct the contextual explanation prompt."""
        arousal = state.get('arousal', 0.5)
        context = "high energy" if arousal > 0.6 else "calm focus"
        
        return f"""You are the Sonic Explainability Agent for the PSYCHE recommendation system.
        
Acknowledge why we are recommending the track '{track_name}' by '{artist}' to the listener. 
The listener is currently in a state of {context}. 

Write exactly ONE punchy, stylish sentence explaining the recommendation. 
Do not use generic phrases like 'we recommended this because'. Instead, say things like 'A high-arousal pulse perfectly suited for your active session.'

Output ONLY the explanation sentence."""
