"""
Emotional State Inference Engine (ESIE) — Gap 1.

Infers the listener's emotional state every 90 seconds using:
1. Ollama/Llama 3.1 8B for full inference
2. Signal-based heuristic fallback
3. Time-of-day heuristic as last resort

Output: ListenerStateVector (valence, arousal, focus, social_mode)
"""

import logging
from typing import Any

from psyche.agents.base import BasePsycheAgent
from psyche.models.listener_state import ListenerStateVector, SessionSignals
from psyche.config import PsycheConfig

logger = logging.getLogger(__name__)


class EmotionalStateInferenceEngine(BasePsycheAgent):
    """
    ESIE — The emotional state inference engine.
    Every 90 seconds, infers the listener's emotional state from session signals.
    """

    def __init__(self, config: PsycheConfig | None = None):
        self._config = config or PsycheConfig.from_yaml()

    @property
    def name(self) -> str:
        return "esie"

    async def infer(self, **kwargs: Any) -> ListenerStateVector:
        """
        Primary inference using Ollama LLM.
        Input: SessionSignals as kwargs
        Output: ListenerStateVector
        """
        import httpx

        signals = SessionSignals(**kwargs)
        prompt = self._build_prompt(signals)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._config.esie.ollama_host}/api/generate",
                json={
                    "model": self._config.esie.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=30.0,
            )
            response.raise_for_status()
            raw = response.json()["response"]

        # Parse LLM output into structured state
        state = self._parse_llm_response(raw, signals)
        return state

    def fallback(self, **kwargs: Any) -> ListenerStateVector:
        """Time-of-day heuristic fallback — always returns valid state."""
        signals = SessionSignals(**kwargs) if kwargs else SessionSignals(
            time_of_day=12.0, day_of_week=0
        )
        tod = signals.time_of_day

        # Time-based heuristic
        if 6 <= tod < 10:    # morning
            valence, arousal, focus = 0.3, 0.2, 0.4
        elif 10 <= tod < 14:  # work hours
            valence, arousal, focus = 0.1, 0.4, 0.7
        elif 14 <= tod < 18:  # afternoon
            valence, arousal, focus = 0.2, 0.3, 0.5
        elif 18 <= tod < 22:  # evening
            valence, arousal, focus = 0.5, 0.5, 0.3
        else:                 # night
            valence, arousal, focus = 0.0, -0.3, 0.2

        social = 0.6 if signals.stated_activity == "social" else 0.2

        return ListenerStateVector(
            valence=valence,
            arousal=arousal,
            focus=focus,
            social_mode=social,
            confidence=0.3,
            method="time_heuristic",
        )

    def _build_prompt(self, signals: SessionSignals) -> str:
        """Build the LLM prompt for ESIE inference."""
        return f"""You are ESIE, the Emotional State Inference Engine for a music recommendation system.

Based on the following listening session signals, infer the listener's emotional state.

Session Signals:
- Time of day: {signals.time_of_day:.1f} (24h format)
- Day of week: {signals.day_of_week} (0=Monday)
- Activity: {signals.stated_activity}
- Recent skips: {signals.recent_skips}
- Recent replays: {signals.recent_replays}
- Session length: {signals.session_length_minutes:.0f} minutes

Output EXACTLY this JSON format (no other text):
{{"valence": <float -1 to 1>, "arousal": <float -1 to 1>, "focus": <float 0 to 1>, "social_mode": <float 0 to 1>, "confidence": <float 0 to 1>}}

Rules:
- valence: -1=very sad, +1=very happy
- arousal: -1=very calm, +1=very energized
- focus: 0=unfocused, 1=deep focus
- social_mode: 0=solitary, 1=very social
- confidence: how confident you are in this estimate"""

    def _parse_llm_response(
        self, raw: str, signals: SessionSignals
    ) -> ListenerStateVector:
        """Parse LLM text output into ListenerStateVector."""
        import json

        try:
            # Try to extract JSON from the response
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start >= 0 and end > start:
                data = json.loads(raw[start:end])
                return ListenerStateVector(
                    valence=max(-1.0, min(1.0, float(data.get("valence", 0.0)))),
                    arousal=max(-1.0, min(1.0, float(data.get("arousal", 0.0)))),
                    focus=max(0.0, min(1.0, float(data.get("focus", 0.5)))),
                    social_mode=max(0.0, min(1.0, float(data.get("social_mode", 0.2)))),
                    confidence=max(0.0, min(1.0, float(data.get("confidence", 0.5)))),
                    method="llm_inference",
                )
        except (json.JSONDecodeError, KeyError, ValueError):
            logger.warning("Failed to parse LLM response, using signal heuristic")

        return self._signal_heuristic(signals)

    def _signal_heuristic(self, signals: SessionSignals) -> ListenerStateVector:
        """Signal-based heuristic — better than time-only but no LLM."""
        skip_ratio = signals.recent_skips / max(1, signals.recent_skips + signals.recent_replays)
        return ListenerStateVector(
            valence=-0.2 if skip_ratio > 0.6 else 0.3,
            arousal=0.5 if signals.stated_activity == "gym" else 0.0,
            focus=0.7 if signals.stated_activity == "work" else 0.3,
            social_mode=0.8 if signals.stated_activity == "social" else 0.2,
            confidence=0.5,
            method="signal_heuristic",
        )
