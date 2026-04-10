# Contributing to PSYCHE

## How to Add a New Agent

1. Create `psyche-core/psyche/agents/your_agent.py`
2. Extend `BasePsycheAgent` from `psyche/agents/base.py`
3. Implement the three required methods:
   - `name` property → agent identifier string
   - `async infer(**kwargs)` → primary inference path (async, typed with Pydantic)
   - `fallback(**kwargs)` → safe fallback when inference fails (MUST return valid output)
4. Create `tests/unit/test_your_agent.py` with tests for:
   - Happy path (inference succeeds)
   - Partial signal (some inputs missing)
   - Full fallback (everything fails — agent still returns valid output)
5. Add W&B logging: `wandb.log({"agent/your_agent/latency_ms": elapsed})`
6. All config values in `configs/config.yaml` — NEVER hardcode
7. Open a PR. CodeRabbit will auto-review.

## Code Standards

```bash
# Before committing:
black .
isort .
mypy psyche-core/psyche/ --ignore-missing-imports
pytest psyche-core/tests/ -v
```

## Commit Message Format

```
feat(agent-name): description
fix(pipeline): description
chore: description
docs: description
test: description
```

## Architecture Rules

- ALL agents extend `BasePsycheAgent`
- ALL data models use Pydantic v2 with `ConfigDict(frozen=True)`
- ALL config via `config.yaml` — never hardcode paths, thresholds, or model names
- ALL experiments log to W&B with git commit hash + DVC data hash
- EVERY agent logs latency and fallback usage
- NEVER let an agent crash the orchestrator — always fallback gracefully
