"""
PSYCHE Config — Pydantic Settings for configuration management.

All configuration loaded from configs/config.yaml with env var overrides.
NEVER hardcode values — always use PsycheConfig.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field


def _load_yaml_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load YAML configuration file."""
    if config_path is None:
        # Search for config relative to project root
        candidates = [
            Path("configs/config.yaml"),
            Path("../configs/config.yaml"),
            Path(__file__).parent.parent.parent / "configs" / "config.yaml",
        ]
        for candidate in candidates:
            if candidate.exists():
                config_path = str(candidate)
                break

    if config_path is None or not Path(config_path).exists():
        return {}

    with open(config_path, "r") as f:
        raw = yaml.safe_load(f) or {}

    # Resolve environment variable references (${VAR_NAME})
    def _resolve_env(value: Any) -> Any:
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_key = value[2:-1]
            return os.environ.get(env_key, value)
        if isinstance(value, dict):
            return {k: _resolve_env(v) for k, v in value.items()}
        if isinstance(value, list):
            return [_resolve_env(v) for v in value]
        return value

    return _resolve_env(raw)


class ESIEConfig(BaseModel):
    """ESIE agent configuration."""

    ollama_model: str = "llama3.1:8b"
    ollama_host: str = "http://localhost:11434"
    update_interval_seconds: int = 90
    fallback_strategy: str = "time_heuristic"


class ColdStartConfig(BaseModel):
    """Cold Start agent configuration."""

    ollama_model: str = "llama3.1:8b"
    num_questions: int = 5
    clap_model: str = "laion/larger_clap_general"


class FairnessConfig(BaseModel):
    """Fairness RL agent configuration."""

    reward_alpha: float = 0.7
    reward_beta: float = 0.2
    reward_gamma: float = 0.1
    underrepresented_regions_exclude: List[str] = ["US", "UK", "SE", "CA", "AU"]
    ppo_policy: str = "MlpPolicy"
    ppo_net_arch: List[int] = [256, 256]
    ppo_total_timesteps: int = 500000
    ppo_checkpoint_interval: int = 50000


class FAISSConfig(BaseModel):
    """FAISS index paths configuration."""

    mert_index_path: str = "data/features/mert_index.faiss"
    mert_id_map_path: str = "data/features/mert_id_map.json"
    clap_index_path: str = "data/features/clap_index.faiss"
    clap_id_map_path: str = "data/features/clap_id_map.json"


class PipelineConfig(BaseModel):
    """Data pipeline configuration."""

    sample_rate: int = 22050
    audio_duration: int = 30
    max_workers: int = 4
    checkpoint_interval: int = 100
    mfcc_coefficients: int = 40
    mert_sample_rate: int = 24000
    clap_sample_rate: int = 48000


class APIConfig(BaseModel):
    """API server configuration."""

    host: str = "0.0.0.0"
    port: int = 8000
    latency_target_p95_ms: int = 200
    api_key: str = ""
    cors_origins: List[str] = ["http://localhost:3000"]


class OrchestratorConfig(BaseModel):
    """Meta-orchestrator configuration."""

    base_weights: Dict[str, float] = {
        "fairness_rl": 0.30,
        "serendipity": 0.25,
        "coherence": 0.25,
        "clap_similarity": 0.20,
    }
    high_arousal_coherence_boost: float = 1.3
    high_focus_serendipity_penalty: float = 0.6
    low_confidence_similarity_boost: float = 1.4


class PsycheConfig(BaseModel):
    """
    Root configuration for the PSYCHE system.
    Loads from configs/config.yaml with environment variable overrides.
    """

    esie: ESIEConfig = ESIEConfig()
    cold_start: ColdStartConfig = ColdStartConfig()
    fairness: FairnessConfig = FairnessConfig()
    faiss: FAISSConfig = FAISSConfig()
    pipelines: PipelineConfig = PipelineConfig()
    api: APIConfig = APIConfig()
    orchestrator: OrchestratorConfig = OrchestratorConfig()

    @classmethod
    def from_yaml(cls, config_path: Optional[str] = None) -> "PsycheConfig":
        """Load config from YAML file with env var resolution."""
        raw = _load_yaml_config(config_path)
        return cls(**{k: v for k, v in raw.items() if k in cls.model_fields})
