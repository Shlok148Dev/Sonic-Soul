# ML Experiment Conventions

## Before Starting Any Experiment
1. Write the hypothesis: "We believe [X] because [Y]. We will test by [Z]."
2. Define the control (what you're comparing against)
3. Define the treatment (what you're testing)
4. Define the decision criterion: "We will adopt treatment if [metric] exceeds [threshold]"
5. Document all of this in EXPERIMENT_LOG.md before running

## W&B Logging Template
```python
import wandb
import subprocess

run = wandb.init(
    project="psyche",
    name="EXP-01-mert-vs-mfcc",
    config={
        "git_commit": subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip(),
        "dvc_hash": "fill_after_dvc_push",
        "model": "mert-95m",
        "dataset": "fma-small",
        "split_strategy": "random",  # or "temporal"
        "random_seed": 42,
    }
)
# ... training ...
wandb.log({"precision_at_10": 0.73, "recall_at_10": 0.68})
wandb.finish()
```

## Validation Split Rules
- Temporal data (LFM-1b, listening history): ALWAYS time-based splits. Train=2008-2021, Val=2022, Test=2023-2024
- Content classification (AudioSet, FMA mood): standard stratified 70/15/15
- NEVER shuffle temporal data before splitting
