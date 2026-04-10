"""
PSYCHE Agent Registry — Factory for creating and wiring all agents.

This is the single place where the orchestrator gets populated with agents.
Called once at startup, never again.
"""

import logging
from typing import Dict, Any

from psyche.config import PsycheConfig
from psyche.orchestrator import PsycheMetaOrchestrator

logger = logging.getLogger(__name__)


def build_orchestrator(config: PsycheConfig | None = None) -> PsycheMetaOrchestrator:
    """
    Create a fully-wired PsycheMetaOrchestrator with all agents registered.
    This is the main entry point for the entire system.
    """
    cfg = config or PsycheConfig.from_yaml()
    orchestrator = PsycheMetaOrchestrator(config=cfg)

    # Import and register all agents
    agents_to_register = []

    try:
        from psyche.agents.esie import EmotionalStateInferenceEngine
        agents_to_register.append(EmotionalStateInferenceEngine(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load ESIE: {e}")

    try:
        from psyche.agents.cold_start import ColdStartPsychographicAgent
        agents_to_register.append(ColdStartPsychographicAgent(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Cold Start: {e}")

    try:
        from psyche.agents.fairness_rl import FairnessAwareRLRecommender
        agents_to_register.append(FairnessAwareRLRecommender(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Fairness RL: {e}")

    try:
        from psyche.agents.sea import SonicExplainabilityAgent
        agents_to_register.append(SonicExplainabilityAgent(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load SEA: {e}")

    try:
        from psyche.agents.serendipity import SerendipityAgent
        agents_to_register.append(SerendipityAgent(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Serendipity: {e}")

    try:
        from psyche.agents.coherence import PlaylistCoherenceArchitect
        agents_to_register.append(PlaylistCoherenceArchitect(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Coherence: {e}")

    try:
        from psyche.agents.integrity import ContentIntegrityGuardian
        agents_to_register.append(ContentIntegrityGuardian(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Integrity: {e}")

    try:
        from psyche.agents.micro_event import MicroEventAttributionEngine
        agents_to_register.append(MicroEventAttributionEngine(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Micro-Event: {e}")

    try:
        from psyche.agents.temporal_taste import TemporalTasteModel
        agents_to_register.append(TemporalTasteModel(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Temporal Taste: {e}")

    try:
        from psyche.agents.context_fusion import ContextFusionModule
        agents_to_register.append(ContextFusionModule(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Context Fusion: {e}")

    try:
        from psyche.agents.intent_classifier import IntentClassifier
        agents_to_register.append(IntentClassifier(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Intent Classifier: {e}")

    try:
        from psyche.agents.rumination_guard import RuminationGuard
        agents_to_register.append(RuminationGuard(config=cfg))
    except Exception as e:
        logger.warning(f"Failed to load Rumination Guard: {e}")

    # Register all
    for agent in agents_to_register:
        orchestrator.register_agent(agent)

    logger.info(
        f"Orchestrator initialized with {len(agents_to_register)} agents: "
        f"{[a.name for a in agents_to_register]}"
    )

    return orchestrator


def get_agent_status(orchestrator: PsycheMetaOrchestrator) -> Dict[str, Any]:
    """Get status of all registered agents."""
    return orchestrator.health()
