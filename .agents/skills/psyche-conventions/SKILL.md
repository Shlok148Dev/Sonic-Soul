# PSYCHE Code Conventions — Every Agent Must Follow These

## Agent Implementation Rules
- ALL agents extend BasePsycheAgent from psyche/agents/base.py
- BasePsycheAgent has three required methods: .infer(), .fallback(), .health_check()
- .infer() is async, fully typed with Pydantic v2 input/output
- .fallback() returns a valid default output when inference fails — NEVER raise an unhandled exception
- EVERY agent logs to W&B via: wandb.log({"agent": "name", "latency_ms": elapsed, "status": "ok"})
- ALL config values come from config.yaml via psyche.config.PsycheConfig — NEVER hardcode paths, thresholds, or model names

## Pydantic Rules
- ALL data models use Pydantic v2 BaseModel
- ALL models have model_config = ConfigDict(frozen=True) for immutable output types
- ALWAYS include Field(..., description="...") on every model field

## Testing Rules
- EVERY agent has a test file at tests/unit/test_{agent_name}.py
- Tests cover: happy path, partial signal fallback, full fallback (agent unavailable)
- pytest -v must pass before any PR is opened

## Experiment Rules
- EVERY experiment run calls: wandb.init(project="psyche", name="EXP-XX-description")
- Log: git commit hash, DVC data hash, all hyperparameters, all metrics
- NEVER use random train/val/test splits on temporal listening data — always time-based

## Error Handling Rules
- EVERY try/except logs the error: logging.error(f"AgentName.infer failed: {e}", exc_info=True)
- EVERY agent falls back gracefully: return self.fallback() on any exception
- NEVER let an agent crash the orchestrator
