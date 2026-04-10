# Global Agent Rules for PSYCHE

1. You are building a production Python ML system, not a demo. Code quality matters.
2. Read SKILL.md files in .agents/skills/ before implementing anything.
3. Never hardcode values. If a value appears twice, it goes in config.yaml.
4. Always run: black . && isort . && mypy psyche/ && pytest tests/ before declaring done.
5. When you finish a task, commit with message format: "feat(agent-name): description"
6. Every new file needs a module-level docstring.
7. If something is unclear, check .agents/skills/ first, then ask — don't guess.
