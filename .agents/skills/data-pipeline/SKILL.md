# Data Pipeline Conventions

## Pipeline Architecture
- ALL pipelines live in psyche-core/psyche/pipelines/
- ALL pipelines use Pydantic v2 models for input/output schemas
- ALL pipelines log progress to W&B
- ALL pipelines support resume from checkpoint

## DVC Rules
- Raw data goes in data/raw/ — NEVER modify raw data
- Validated data goes in data/validated/
- Features go in data/features/
- Models go in data/models/
- ALL data outputs MUST be DVC tracked: `dvc add <path>`
- After DVC add: `git add <path>.dvc .gitignore && git commit`

## Quality Gates
- Validate ALL audio files with librosa.load() before processing
- Quarantine corrupt files to data/quarantine/ with logged reason
- Log: total_files, valid_count, corrupt_count, validation_rate to W&B
- Target: <1% invalid files in any batch

## Checkpoint Resume
- Save progress every 100 tracks for long-running pipelines
- Use parquet for intermediate checkpoints (efficient, columnar)
- Track which track IDs are already processed to enable resume
- Log checkpoint saves to W&B

## Parallel Processing
- Use concurrent.futures.ProcessPoolExecutor for CPU-bound work
- Default max_workers=4 (configurable in config.yaml)
- Use asyncio for I/O-bound work (API calls, file reads)
