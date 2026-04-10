---
name: New Agent Request
about: Propose a new PSYCHE agent
title: '[AGENT] '
labels: enhancement, agent
assignees: ''
---

## Agent Name
<!-- e.g., SleepQualityAgent -->

## What Gap/Addition Does It Address?
<!-- Reference a specific Gap (1-10) or Addition (01-60) from the masterplan -->

## Input Signals
<!-- What data does this agent consume? -->
- Signal 1: ...
- Signal 2: ...

## Output Schema
<!-- What does the agent return? -->
```python
class AgentOutput(BaseModel):
    ...
```

## Fallback Behavior
<!-- What happens when inference fails? -->

## Success Metrics
<!-- How do we know it works? -->
- Metric 1: ...
- Metric 2: ...

## Implementation Notes
<!-- Any specific models, datasets, or approaches? -->
