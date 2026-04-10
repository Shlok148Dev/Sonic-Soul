"""
Cold Start Psychographic Agent — Gap 3.

Conducts a 5-question conversational interview to build an initial
Sonic Identity for new users, replacing the generic "pick 3 genres" approach.

Uses SSE streaming for typewriter-effect delivery to the frontend.
"""

import logging
from typing import Any, Dict, List

from psyche.agents.base import BasePsycheAgent
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)

# The 5 psychographic questions (from the masterplan)
COLD_START_QUESTIONS: List[str] = [
    "When do you use music most? Work, gym, commuting, sleep — tell me about the soundtrack of your day.",
    "Think of a song that never gets old for you, no matter how many times you've heard it. What is it, and what does it make you feel?",
    "Imagine you're hosting a small dinner party with 6 close friends. What kind of music are you putting on?",
    "Here's an unusual one: if your emotional state today were a weather pattern, what would it be? Sunny, stormy, foggy?",
    "Last one — are you more of a 'deep cuts' person who loves finding obscure tracks, or do you prefer the comfort of popular, well-known music?",
]


class ColdStartPsychographicAgent(BasePsycheAgent):
    """
    Cold Start Agent — builds initial Sonic Identity through conversational interview.
    Each answer morphs the Sonic Identity radar in real time.
    """

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "cold_start"

    async def infer(self, **kwargs: Any) -> Dict[str, Any]:
        """
        Process a user's answer and return the next question + radar delta.
        Input: turn (int), user_answer (str), user_id (str)
        Output: {next_question, radar_delta, agent_response, interview_complete}
        """
        import httpx

        turn: int = kwargs.get("turn", 1)
        user_answer: str = kwargs.get("user_answer", "")
        user_id: str = kwargs.get("user_id", "anonymous")

        if turn > self._config.cold_start.num_questions:
            return {
                "next_question": None,
                "radar_delta": {},
                "agent_response": "Your Sonic Identity is ready. Initializing PSYCHE...",
                "interview_complete": True,
            }

        # Use Ollama to analyze the answer and generate radar adjustments
        prompt = self._build_analysis_prompt(turn, user_answer)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._config.esie.ollama_host}/api/generate",
                json={
                    "model": self._config.cold_start.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            analysis = response.json()["response"]

        radar_delta = self._parse_radar_delta(analysis, turn)

        next_q = (
            COLD_START_QUESTIONS[turn]
            if turn < len(COLD_START_QUESTIONS)
            else None
        )

        return {
            "next_question": next_q,
            "radar_delta": radar_delta,
            "agent_response": analysis,
            "interview_complete": turn >= self._config.cold_start.num_questions,
        }

    def fallback(self, **kwargs: Any) -> Dict[str, Any]:
        """Fallback — return the next question without LLM analysis."""
        turn: int = kwargs.get("turn", 1)

        if turn > 5:
            return {
                "next_question": None,
                "radar_delta": {},
                "agent_response": "Your Sonic Identity is ready.",
                "interview_complete": True,
            }

        # Default radar adjustments per question
        default_deltas = [
            {"harmonic_complexity": 0.2, "rhythmic_drive": 0.2},
            {"emotional_depth": 0.3, "harmonic_complexity": 0.1},
            {"social_mode": 0.4, "discovery_hunger": 0.1},
            {"emotional_depth": 0.2, "rhythmic_drive": 0.1},
            {"discovery_hunger": 0.4},
        ]

        next_q = (
            COLD_START_QUESTIONS[turn]
            if turn < len(COLD_START_QUESTIONS)
            else None
        )

        return {
            "next_question": next_q,
            "radar_delta": default_deltas[min(turn - 1, 4)],
            "agent_response": "Great answer! Let me adjust your Sonic Identity...",
            "interview_complete": turn >= 5,
        }

    def _build_analysis_prompt(self, turn: int, answer: str) -> str:
        """Build LLM prompt for analyzing user's cold start answer."""
        return f"""You are the Cold Start Psychographic Agent for PSYCHE, a music intelligence system.

The user was asked question #{turn}: "{COLD_START_QUESTIONS[turn - 1]}"
Their answer: "{answer}"

Based on this answer, provide:
1. A warm, insightful 1-2 sentence response acknowledging their answer
2. Determine adjustments to their Sonic Identity radar axes:
   - harmonic_complexity (0-1): preference for complex harmonies vs simple
   - rhythmic_drive (0-1): preference for rhythm-forward music
   - emotional_depth (0-1): preference for emotionally intense music
   - discovery_hunger (0-1): desire for new/unfamiliar music
   - social_mode (0-1): listening as social vs solitary activity

Output ONLY a JSON object:
{{"response": "your warm response", "radar_delta": {{"axis_name": delta_value, ...}}}}

Keep the response conversational and music-knowledgeable. Never be generic."""

    def _parse_radar_delta(self, analysis: str, turn: int) -> Dict[str, float]:
        """Parse the LLM response into radar delta values."""
        import json

        try:
            start = analysis.find("{")
            end = analysis.rfind("}") + 1
            if start >= 0 and end > start:
                data = json.loads(analysis[start:end])
                return data.get("radar_delta", {})
        except (json.JSONDecodeError, KeyError):
            pass

        return self.fallback(turn=turn)["radar_delta"]
