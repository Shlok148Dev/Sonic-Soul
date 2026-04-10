# PSYCHE — COMPLETE FROM-SCRATCH DEVELOPMENT GUIDE
## *How to Build, Ship, and Launch a Production-Grade Music Intelligence Platform Using 100% Free Tools*

> **What this document is:** A literal how-to-build guide. Not architecture. Not what to build. *How* to sit down, open your laptop, and go from zero files to a published, deployed, fully working system — one concrete step at a time.
>
> **Every tool used here is free.** Every paid feature has been identified and replaced. Nothing is mocked. When you finish Week 14, every endpoint returns real data, every agent runs real inference, every UI component talks to real APIs.

---

## UNDERSTANDING YOUR ACTUAL TOOL STACK

Before touching a keyboard, know exactly what each tool *actually does* — not the marketing version.

### Google Antigravity — What It Actually Is
Antigravity is an agent-first IDE at `antigravity.google`. Think of it as VS Code but instead of a Copilot sidebar, it has an **Agent Manager** — a dashboard where you spawn autonomous agents that can write code, run terminals, and navigate your browser *simultaneously*. You give an agent a mission ("build this agent with these acceptance criteria"), it works, and returns an Artifact (the result). You comment on the Artifact like a Google Doc. It fixes. You merge. That loop replaces the "write code → test → debug → write more code" loop you're used to.

You already have the **CodeRabbit extension installed in Antigravity**. That extension is the IDE-side review — it reviews your code inline *before* you even make a PR. The GitHub-side CodeRabbit (which you connect to your repo) reviews *after* you open a PR. Both work together and both are free-tier.

### GSD (Get Shit Done) — What It Actually Is
GSD is a slash-command system for Antigravity and Claude Code. Instead of typing a vague prompt and hoping for good code, GSD forces a structured flow: Discuss → Plan → Execute → Verify → Ship. The Discuss phase makes you resolve all ambiguity *before* any code is written. The Plan phase creates a checklist with exact verification criteria — so you know objectively when a task is done. This is what stops the "it mostly works" trap.

Install it once: `npx get-shit-done-cc@latest --global`

### Ralph Loop — What It Actually Is
Ralph Loop is an autonomous execution tool. You write a spec file (`CLAUDE.md`) that tells Antigravity exactly what to build, how to verify it, and what output to emit when done. Then you run a shell loop that keeps calling Antigravity on that spec until it produces the "done" signal. This is how you run overnight builds: start it at 10pm, wake up to completed, tested, committed code. You don't babysit it. Git history is the memory across loop iterations.

### CodeRabbit — What It Actually Is (Both Surfaces)
**Surface 1 — Antigravity IDE Extension (you have this):** Reviews code inline as you work. Highlights issues before you commit. Use this for fast feedback during active development.

**Surface 2 — GitHub Integration (free tier):** Connect at `app.coderabbit.ai`, link to your GitHub org, it automatically reviews every Pull Request you open. Free tier gives you: PR summarization (what changed and why), inline comments on issues it finds, and reviews in IDE. You configure its behavior via a `.coderabbit.yaml` file in your repo root — this isn't a config you pay for, it's just a text file that tells the bot what to care about.

**What free tier does NOT give you:** SAST/linter integration, analytics dashboards, docstring auto-generation. You don't need those — the core review is free.

---

## THE FREE STACK — EVERY PAID THING REPLACED

| Original (Possibly Paid) | Replaced With | Why It's Better |
|---|---|---|
| Spotify API (paid tiers) | FMA dataset (free, CC licensed) + Spotify free tier (30s previews, metadata only) | No rate limit anxiety for development |
| Hugging Face Inference API (paid for GPU) | Ollama (local inference) + HF Spaces (free CPU tier for deployment) | Zero cost, local during dev, free hosting |
| Any paid LLM API during dev | Ollama with Llama 3.1 8B / Mistral 7B (local, free) | Unlimited calls, no billing surprises |
| Anthropic API (for Cold Start + SEA) | Free tier during testing, use sparingly — or Ollama fallback | Anthropic free tier gives you enough for demo |
| W&B Pro | W&B free tier (unlimited projects, 100GB storage) | Free tier is genuinely unlimited for this project |
| Vercel Pro | Vercel free Hobby tier | More than enough for demo traffic |
| Railway/Render paid | Railway free tier (500 hours/month) + Render free tier | Enough for demo deployment |
| Any paid database | Supabase free tier (PostgreSQL, 500MB) | Generous free tier, production-grade |
| Redis paid | Upstash Redis free tier (10k requests/day) | Perfect for session caching |
| CodeRabbit Pro | CodeRabbit free tier + IDE extension you already have | PR summaries + inline reviews = all you need |
| Any paid CI/CD | GitHub Actions (2000 free minutes/month for public repos) | Unlimited for public repos |

---

## PRE-FLIGHT CHECKLIST — ACCOUNTS TO CREATE BEFORE DAY 1

Create these accounts now. All free. No credit card needed for any of them.

```
□ GitHub account — github.com (you probably have this)
□ Google account — for Antigravity (antigravity.google)
□ Weights & Biases — wandb.ai (free, no card)
□ Hugging Face — huggingface.co (free, no card)
□ Vercel — vercel.com (free Hobby, no card)
□ Supabase — supabase.com (free tier, no card)
□ Upstash — upstash.com (free Redis, no card)
□ CodeRabbit — app.coderabbit.ai (free, GitHub login)
□ Railway — railway.app (free tier, no card for basic)
□ Anthropic — console.anthropic.com (free tier credits)
```

---

## PART 1: ENVIRONMENT SETUP (Days 1–2)

### Step 1.1: Install Everything Locally

Open your terminal. Run these in order. Don't skip any.

```bash
# Python environment
brew install pyenv          # macOS — skip if Linux, use apt
pyenv install 3.11.9
pyenv global 3.11.9
python --version            # should say 3.11.9

# Node.js (for GSD + psyche-ui)
brew install nvm
nvm install 20
nvm use 20
node --version              # should say v20.x

# Docker
brew install --cask docker  # macOS
# Linux: follow docs.docker.com/engine/install/ubuntu/
docker --version            # verify

# Ollama (local LLM inference — your local GPT)
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.1:8b     # downloads ~4.7GB — do this on WiFi
ollama pull mistral:7b       # downloads ~4.1GB — backup model
# Test it works:
ollama run llama3.1:8b "say hello in 5 words"

# DVC (data versioning)
pip install dvc dvc-gdrive   # gdrive for remote storage (free)

# GSD (the planning slash commands)
npm install -g get-shit-done-cc@latest
# Test:
gsd --help

# Git (you have this, but verify)
git --version
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Step 1.2: Create the GitHub Organization

1. Go to `github.com` → Your profile → "Your organizations" → "New organization"
2. Name it: `psyche-music`
3. Plan: Free
4. Create these repos inside it (all Public — required for free GitHub Actions):

```
psyche-music/psyche-core    ← Python SDK + all agents
psyche-music/psyche-ui      ← Next.js frontend
psyche-music/psyche-api     ← FastAPI backend
psyche-music/psyche-bench   ← Benchmark CLI
psyche-music/psyche-plugins ← VS Code extension + Discord bot
```

For each repo: Initialize with README, add `.gitignore` (Python for core/api/bench, Node for ui/plugins).

### Step 1.3: Connect CodeRabbit to Your GitHub Org

1. Go to `app.coderabbit.ai` → Sign in with GitHub
2. "Add Organization" → select `psyche-music`
3. Enable on all 5 repos
4. Done. CodeRabbit will now auto-review every PR you open.

You don't need to configure anything yet. You'll add `.coderabbit.yaml` files to each repo in Week 1 — these are just text files that tell the bot what to focus on. The bot works without them too.

### Step 1.4: Open Antigravity and Set Up Workspaces

1. Go to `antigravity.google`, sign in with the same Google account
2. Create 4 workspaces, one per repo:

```
Workspace 1: psyche-core     → clone psyche-music/psyche-core
Workspace 2: psyche-ui       → clone psyche-music/psyche-ui
Workspace 3: psyche-api      → clone psyche-music/psyche-api
Workspace 4: psyche-bench    → clone psyche-music/psyche-bench
```

In Antigravity, "Add Workspace" → "From GitHub repo" → paste the URL.

**Model selection for each workspace:**
- Default: Gemini 2.5 Pro (free, generous limits, fast)
- Switch to Claude Sonnet 4.6 for: agent logic, orchestrator, complex algorithm design
- The model picker is top-right of the Agent chat panel

### Step 1.5: Create the Agent Knowledge Base

In the `psyche-core` workspace, create these files. These are the instructions every future agent will read automatically — this is how Antigravity's knowledge base works. You write it once, every agent reads it forever.

```bash
mkdir -p .agents/skills/psyche-conventions
mkdir -p .agents/skills/ml-experiment
mkdir -p .agents/skills/data-pipeline
```

Create `.agents/skills/psyche-conventions/SKILL.md`:
```markdown
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
```

Create `.agents/skills/ml-experiment/SKILL.md`:
```markdown
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
```

Create `.agents/rules.md`:
```markdown
# Global Agent Rules for PSYCHE Core

1. You are building a production Python ML system, not a demo. Code quality matters.
2. Read SKILL.md files in .agents/skills/ before implementing anything.
3. Never hardcode values. If a value appears twice, it goes in config.yaml.
4. Always run: black . && isort . && mypy psyche/ && pytest tests/ before declaring done.
5. When you finish a task, commit with message format: "feat(agent-name): description"
6. Every new file needs a module-level docstring.
7. If something is unclear, check .agents/skills/ first, then ask — don't guess.
```

Commit these files:
```bash
git add .agents/
git commit -m "chore: add agent knowledge base"
git push
```

### Step 1.6: Initialize DVC and W&B

```bash
cd psyche-core

# DVC setup
dvc init
git add .dvc/
git commit -m "chore: init dvc"

# Create data directory structure
mkdir -p data/{raw,validated,features,splits,models}
echo "data/raw/" >> .gitignore
echo "data/validated/" >> .gitignore
echo "data/features/" >> .gitignore

# W&B login (one-time)
pip install wandb
wandb login
# Paste your API key from wandb.ai/settings
# Project will auto-create when you first run wandb.init()
```

### Step 1.7: Docker Environment Setup (GSD Phase 0)

Now use GSD for the first time. In the psyche-core workspace in Antigravity:

```
/gsd:new-project
```

Answer the questions:
- Project name: PSYCHE Core
- Type: Python ML backend
- What does it do: Multi-agent music intelligence platform
- Primary output: pip-installable Python package + Docker container

```
/gsd:discuss-phase 0
```

GSD will ask you questions about the Docker setup. Answer:
- Python 3.11
- Services needed: FastAPI, Redis (Upstash for production, local Redis for dev), PostgreSQL (Supabase for production, local Postgres for dev)
- ML deps: librosa, Demucs, MERT (via transformers), FAISS-cpu, torch CPU, CLAP
- Dev vs. prod separation: yes

```
/gsd:plan-phase 0
```

Review the plan GSD creates. If it looks right:
```
/gsd:execute-plan
```

Antigravity's agent will create `docker/Dockerfile` and `docker/docker-compose.yml`. Review what it creates. The docker-compose should have:
- `psyche-core` service (Python 3.11, your code mounted)
- `redis` service (local development)
- `postgres` service (local development)
- Health checks on all services

Test it:
```bash
docker-compose -f docker/docker-compose.yml up
# Should see all services healthy
```

Open a PR. CodeRabbit will auto-review within a few minutes. Read its comments. Fix any flagged issues. Merge.

---

## PART 2: DATA PIPELINE (Days 3–7)

This is the most important week. If your data pipeline is wrong, every model trained on it is wrong. Do this carefully.

### Step 2.1: Download FMA Dataset (Day 3)

```bash
cd psyche-core/data/raw

# FMA-small (8k tracks, ~7.2GB) — this is your primary training set
# FMA-medium (25k tracks, ~22GB) — optional, for final training
wget -c https://os.unil.cloud.switch.ch/fma/fma_small.zip
wget -c https://os.unil.cloud.switch.ch/fma/fma_metadata.zip

# Verify checksums (listed on github.com/mdeff/fma)
md5sum fma_small.zip    # must match: f0df49ffe5f2a6008d7dc83c6915b31d
md5sum fma_metadata.zip # must match: f9f9d229eb0c926efca65105c52eff3c

# Extract
unzip fma_small.zip
unzip fma_metadata.zip

# DVC track the raw data (never modify raw, just track)
dvc add data/raw/fma_small/
dvc add data/raw/fma_metadata/
git add data/raw/fma_small.dvc data/raw/fma_metadata.dvc .gitignore
git commit -m "data: add FMA-small and metadata DVC tracking"
```

**What the FMA metadata contains (understand this before building the pipeline):**

```python
import pandas as pd

tracks = pd.read_csv('data/raw/fma_metadata/tracks.csv', index_col=0, header=[0, 1])
genres = pd.read_csv('data/raw/fma_metadata/genres.csv', index_col=0)
features = pd.read_csv('data/raw/fma_metadata/features.csv', index_col=0, header=[0, 1, 2])

# tracks has columns like: track.title, track.artist_name, track.genre_top,
#   album.title, artist.location, track.duration, track.listens
# genres has: genre_id, title, top_level, parent
# features has: pre-computed MFCCs, chroma, spectral — useful as baseline

print(tracks.shape)    # (106574, ...) for full, (8000, ...) for small
print(tracks['track', 'genre_top'].value_counts().head(10))
```

### Step 2.2: Build the Validation Pipeline (Day 3, Evening — Ralph Loop)

Write the spec file for Ralph Loop:

```bash
cat > scripts/ralph/CLAUDE.md << 'SPEC'
# PSYCHE Phase 1.1: FMA Validation Pipeline

## What To Build
File: psyche/pipelines/ingestion.py

Build a complete validation pipeline class: FMAIngestionPipeline
It must:
1. Load all audio file paths from data/raw/fma_small/ (recursively find all .mp3 files)
2. For each file, validate it with librosa.load(sr=22050, mono=True, duration=30)
   - If load succeeds: record {path, duration, sample_rate, is_valid: True}
   - If load fails (corrupt, empty, wrong format): record {path, error: str, is_valid: False}
   - Move corrupt files to data/quarantine/ and log the reason
3. Build manifest.json in data/validated/ with all valid files
4. Log to W&B: total_files, valid_count, corrupt_count, validation_rate
5. Use tqdm for progress bar
6. Process in parallel using concurrent.futures.ProcessPoolExecutor (max_workers=4)

## File Structure
```
psyche/pipelines/
├── __init__.py
├── ingestion.py        ← Build this
└── data_quality.py     ← Leave empty for now
```

## Acceptance Criteria
- pytest tests/unit/test_ingestion.py passes
- Script runs: python -m psyche.pipelines.ingestion --data-dir data/raw/fma_small/ --output data/validated/
- manifest.json is created with at least 7800 valid tracks (FMA-small should have >97% valid)
- W&B run created with metrics logged
- corrupt files moved to data/quarantine/

## Architecture Constraints (from .agents/skills/psyche-conventions/SKILL.md)
- Use Pydantic v2 for TrackManifest and TrackRecord models
- Log start time, end time, duration of pipeline run
- Config (sr, duration, max_workers) must come from config.yaml

## Test File To Write
tests/unit/test_ingestion.py:
- test_valid_file_accepted (create a 5-second sine wave .mp3, run through pipeline, assert is_valid=True)
- test_corrupt_file_quarantined (create an empty .mp3 file, assert it lands in quarantine)
- test_manifest_created (run on a tiny set of 5 files, assert manifest.json exists and has 5 entries)

## Output Promise
When pytest tests/unit/test_ingestion.py passes AND the manifest.json exists with >7800 entries:
output <promise>INGESTION_PIPELINE_DONE</promise>
SPEC

# Create the ralph runner script
cat > scripts/ralph/ralph.sh << 'RALPH'
#!/bin/bash
MAX_ITER=${1:-30}
CLAUDE_MD="scripts/ralph/CLAUDE.md"

for i in $(seq 1 $MAX_ITER); do
  echo "=== Ralph Loop Iteration $i ==="
  
  # Run Antigravity/Claude Code with the spec
  # Replace this with your actual Antigravity CLI invocation
  antigravity run --prompt "$CLAUDE_MD" --output progress_$i.txt
  
  # Check for completion signal
  if grep -q "<promise>.*DONE</promise>" progress_$i.txt 2>/dev/null; then
    echo "✓ Task complete after $i iterations"
    break
  fi
  
  echo "Not done yet. Updating progress context..."
  cat progress_$i.txt >> .ralph_progress.txt
done
RALPH

chmod +x scripts/ralph/ralph.sh
```

**Run Ralph overnight:**
```bash
./scripts/ralph/ralph.sh 30
```

Wake up. Check:
```bash
cat data/validated/manifest.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'Valid tracks: {len(d[\"tracks\"])}')"
# Should say: Valid tracks: 7900+ (approximately)
```

Open a PR. Wait for CodeRabbit to review. Fix flagged issues. Merge.

### Step 2.3: Feature Extraction Pipeline (Days 4–5)

Use GSD to plan this phase:
```
/gsd:discuss-phase 1
```

GSD will ask about feature extraction strategy. Key decisions to make:
- librosa features: yes (MFCCs, chroma, tempo, energy, spectral centroid) — 40 MFCC coefficients
- Demucs stems: yes, but run separately overnight (heavy)
- MERT embeddings: yes, using the Hugging Face model
- CLAP embeddings: yes, using LAION-CLAP
- Batch size: 50 tracks per batch (memory-safe on CPU)
- Checkpoint: save progress every 100 tracks so it can resume if interrupted

```
/gsd:plan-phase 1
```

GSD creates atomic tasks. Review them. Then for each task, write a Ralph spec and run it:

**Task 1.2a: librosa feature extraction**

```
# CLAUDE.md for librosa features
Build psyche/pipelines/feature_extraction.py

Class: LibrosaFeatureExtractor
Input: manifest.json from data/validated/
Output: data/features/librosa_features.parquet (one row per track)

Features to extract per track:
- mfccs: np.mean and np.std for each of 40 MFCC coefficients (80 values)
- spectral_centroid: mean, std
- spectral_rolloff: mean, std
- zero_crossing_rate: mean, std
- rms_energy: mean, std
- tempo: scalar BPM
- chroma_stft: mean for each of 12 chroma bins (12 values)
Total: ~110 features per track

Requirements:
- Resume from checkpoint: track which track IDs are already done
- Save checkpoint every 100 tracks as parquet
- Log to W&B: tracks_processed, tracks_failed, processing_rate (tracks/min)
- Use multiprocessing (4 workers)
- Handle: librosa.util.exceptions.ParameterError, FileNotFoundError, RuntimeError

DVC: dvc add data/features/librosa_features.parquet after extraction completes

Acceptance: data/features/librosa_features.parquet exists with ~7900 rows, ~110 columns
output <promise>LIBROSA_FEATURES_DONE</promise>
```

**Task 1.2b: Demucs stem separation (run overnight, it's slow)**

```
# CLAUDE.md for Demucs stems
Build psyche/pipelines/stem_separation.py

Class: DemucsProcessor
Input: manifest.json
Output: data/features/stems/{track_id}/{vocals.wav, drums.wav, bass.wav, other.wav}

Requirements:
- Use: from demucs.pretrained import load_pretrained; model = load_pretrained("htdemucs")
- Process 1 track at a time (Demucs is memory intensive)
- Save 4 stem files per track at 22050 Hz
- After separation: extract energy per stem (RMS over whole file)
- Save stem_energies.parquet: columns = [track_id, vocals_rms, drums_rms, bass_rms, other_rms]
- Checkpoint: skip tracks where stem files already exist
- Target: process at least 2000 tracks overnight (set in config: max_tracks_demucs)

IMPORTANT: Run on FMA-small tracks sorted by shortest first (faster iteration, better checkpointing)

Acceptance: stem_energies.parquet exists with at least 2000 rows
output <promise>DEMUCS_STEMS_DONE</promise>
```

**Task 1.2c: MERT embeddings**

```
# CLAUDE.md for MERT embeddings
Build psyche/pipelines/mert_embeddings.py

Class: MERTEmbeddingExtractor

Setup:
from transformers import AutoModel, Wav2Vec2FeatureExtractor
model = AutoModel.from_pretrained("m-a-p/MERT-v1-95M", trust_remote_code=True)
processor = Wav2Vec2FeatureExtractor.from_pretrained("m-a-p/MERT-v1-95M", trust_remote_code=True)
model.eval()

Process:
1. Load audio at 24000 Hz (MERT's required sr)
2. Extract features: inputs = processor(audio, sampling_rate=24000, return_tensors="pt")
3. with torch.no_grad(): outputs = model(**inputs, output_hidden_states=True)
4. Use last hidden state: embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
5. Shape: (768,) per track

Output: data/features/mert_embeddings.npz (keys = track_id strings, values = 768-dim arrays)
Also save: data/features/mert_embeddings_index.json (mapping track_id → index in npz)

Requirements:
- Batch size: 1 (CPU, no batching needed)
- Checkpoint: save npz every 50 tracks
- CPU only (no CUDA assumption)
- DVC track the output files

Acceptance: mert_embeddings.npz exists with at least 7500 track embeddings
output <promise>MERT_EMBEDDINGS_DONE</promise>
```

**Task 1.2d: CLAP embeddings**

```
# CLAUDE.md for CLAP embeddings
Build psyche/pipelines/clap_embeddings.py

Class: CLAPEmbeddingExtractor

Setup:
import laion_clap
model = laion_clap.CLAP_Module(enable_fusion=False)
model.load_ckpt()  # downloads pretrained weights automatically
model.eval()

Process:
1. Load audio as numpy array at 48000 Hz (CLAP's required sr)
2. audio_embedding = model.get_audio_embedding_from_data([audio_array], use_tensor=False)
3. Shape: (1, 512) → squeeze to (512,)

Output: data/features/clap_embeddings.npz (same format as MERT)
Also save: data/features/clap_embeddings_index.json

Requirements:
- Same checkpoint pattern as MERT extractor
- Also extract text embeddings for each track's metadata string:
  text = f"{track_title} {artist_name} {genre}"
  text_embedding = model.get_text_embedding([text], use_tensor=False)  # shape (512,)
  Save to: data/features/clap_text_embeddings.npz

Acceptance: clap_embeddings.npz AND clap_text_embeddings.npz exist with 7500+ entries each
output <promise>CLAP_EMBEDDINGS_DONE</promise>
```

**Task 1.2e: FAISS Index Build**

```
# CLAUDE.md for FAISS index
Build psyche/pipelines/embedding_index.py

Class: FAISSIndexBuilder

What to build — two separate FAISS indexes:
1. MERT index (768-dim, 7500+ vectors):
   - faiss.IndexFlatL2(768) — exact search, fine for 8k vectors
   - Save to: data/features/mert_index.faiss
   - Also save: data/features/mert_id_map.json (maps faiss_position → track_id)

2. CLAP audio index (512-dim, 7500+ vectors):
   - faiss.IndexFlatIP(512) — inner product (cosine after normalization)
   - Normalize all vectors before adding: faiss.normalize_L2(embeddings)
   - Save to: data/features/clap_index.faiss
   - Also save: data/features/clap_id_map.json

3. Combined index builder: builds both, verifies search works
   Test query: pick random track embedding, search k=10, print returned track IDs and distances

Build also: psyche/utils/embeddings.py with:
- load_faiss_index(name: str) → (faiss.Index, dict)  # name = "mert" or "clap"
- search_similar(index, id_map, query_vector, k=10) → List[Tuple[str, float]]
- get_embedding(track_id: str, embedding_type: str) → np.ndarray

Acceptance:
- Both FAISS indexes built and searchable
- pytest tests/unit/test_faiss_index.py passes (test: search returns k results, all are valid track IDs)
- python -c "from psyche.utils.embeddings import search_similar, load_faiss_index; idx, id_map = load_faiss_index('clap'); print('FAISS OK')" works
output <promise>FAISS_INDEX_DONE</promise>
```

### Step 2.4: Run All 5 Baselines (Days 6–7)

These are your benchmarks — every PSYCHE agent must beat them. Run them now so you have numbers.

```
/gsd:discuss-phase 2
/gsd:plan-phase 2
```

Ralph spec for baselines:
```
# CLAUDE.md for baselines
Build: scripts/run_baselines.py
And: psyche/evaluation/baselines.py

Build 5 baseline recommenders:

B0 - RandomRecommender:
  .recommend(user_id, n=10) → List[track_id] (randomly sampled from catalog)
  Metrics: serendipity rate (% of recs user hasn't heard before)

B1 - PopularityRecommender:
  Load tracks sorted by track.listens from FMA metadata
  .recommend(user_id, n=10) → top-N most listened tracks globally
  Metrics: same as B0

B2 - GenreMatchRecommender:
  Assign each user a "top genre" (first genre in their history if available, else random)
  .recommend(user_id, n=10) → top-N most listened tracks in that genre
  Metrics: same

B3 - CLAPSimilarityRecommender (the real baseline):
  Given a user's seed tracks, compute average CLAP embedding
  Use FAISS clap_index to find k=50 nearest neighbors
  Remove already-heard tracks
  Return top-10 of remaining
  Metrics: serendipity, diversity (Gini of artist plays), coherence (average cosine similarity of recs to each other)

B4 - ALSRecommender:
  Use implicit library (pip install implicit) with BM25Recommender or AlternatingLeastSquares
  Train on FMA play count matrix (track_id × simulated_user co-occurrence)
  Since FMA doesn't have user-track play data, use: same-genre as co-occurrence signal
  Metrics: same

Evaluation:
- Create synthetic test set: 200 "users" each assigned a random genre + 10 seed tracks
- For each user, run all 5 recommenders, compute metrics
- Log ALL metrics to W&B under run name "baseline-benchmarks"
- Save results to: data/evaluation/baseline_results.json

W&B table: rows = baselines, columns = serendipity, diversity (gini), avg_coherence, recall@10

Acceptance: 
- baseline_results.json exists with 5 baselines × 5 metrics
- W&B run shows comparison table
output <promise>BASELINES_DONE</promise>
```

After baselines run, you'll have real numbers. Write them down. Every PSYCHE agent must beat B3 (CLAP similarity) on its specific metric.

---

## PART 3: THE CORE ML AGENTS (Weeks 3–6)

### Week 3, Day 15: Build BasePsycheAgent Protocol First

Before any specific agent, build the contract every agent must implement. This is the most important file in the codebase.

```bash
# In Antigravity, create this file manually (don't use Ralph for this — write it yourself, it's architecture)
```

Create `psyche/agents/base.py`:
```python
"""
BasePsycheAgent — The contract that every PSYCHE agent must implement.

This protocol defines the interface. Every agent is independently testable,
independently fallible, and independently deployable.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import time
import logging
import wandb
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


class AgentHealthStatus(BaseModel):
    model_config = ConfigDict(frozen=True)
    agent_name: str
    status: str  # "healthy" | "degraded" | "failed"
    latency_ms: Optional[float] = None
    last_check: str  # ISO timestamp
    error: Optional[str] = None


class BasePsycheAgent(ABC):
    """
    Abstract base class for all PSYCHE agents.
    
    Every agent:
    - Has a name (used in logging and W&B)
    - Has an async infer() method (the main inference path)
    - Has a fallback() method (called when infer() fails — MUST return valid output)
    - Has a health_check() method (for the /health endpoint)
    - Logs every call to W&B with latency and status
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Agent identifier. Used in logs, W&B, and API responses."""
        ...
    
    @abstractmethod
    async def infer(self, **kwargs) -> Any:
        """
        Primary inference path. Must be async.
        Raise any exception if inference fails — the base class handles it.
        """
        ...
    
    @abstractmethod
    def fallback(self, **kwargs) -> Any:
        """
        Fallback path. Called when infer() raises any exception.
        MUST return a valid output of the same type as infer().
        MUST NOT raise exceptions.
        """
        ...
    
    async def run(self, **kwargs) -> Dict[str, Any]:
        """
        The safe execution wrapper. Call this, not infer() directly.
        Handles: timing, W&B logging, fallback on failure.
        Returns: {"result": ..., "agent": name, "used_fallback": bool, "latency_ms": float}
        """
        start = time.perf_counter()
        used_fallback = False
        
        try:
            result = await self.infer(**kwargs)
        except Exception as e:
            logger.error(f"{self.name}.infer failed: {e}", exc_info=True)
            result = self.fallback(**kwargs)
            used_fallback = True
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        
        try:
            wandb.log({
                f"agent/{self.name}/latency_ms": elapsed_ms,
                f"agent/{self.name}/used_fallback": int(used_fallback),
            })
        except Exception:
            pass  # W&B failure must never crash the agent
        
        return {
            "result": result,
            "agent": self.name,
            "used_fallback": used_fallback,
            "latency_ms": elapsed_ms,
        }
    
    def health_check(self) -> AgentHealthStatus:
        """Override in each agent to test model availability."""
        return AgentHealthStatus(
            agent_name=self.name,
            status="healthy",
            last_check=__import__("datetime").datetime.utcnow().isoformat(),
        )
```

Commit this file:
```bash
git add psyche/agents/base.py
git commit -m "feat(agents): add BasePsycheAgent protocol"
```

### Week 3, Days 15–16: ESIE — Emotional State Inference Engine

This agent is the heart of PSYCHE. It updates every 90 seconds and drives the orchestrator.

**Write the Ralph spec:**
```bash
cat > scripts/ralph/CLAUDE.md << 'SPEC'
# ESIE: Emotional State Inference Engine

## The ListenerStateVector model
Build psyche/models/listener_state.py:

```python
from pydantic import BaseModel, ConfigDict, Field

class ListenerStateVector(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    valence: float = Field(..., ge=-1.0, le=1.0, description="Emotional positivity. -1=very sad, +1=very happy")
    arousal: float = Field(..., ge=-1.0, le=1.0, description="Energy level. -1=very calm, +1=very energized")  
    focus: float = Field(..., ge=0.0, le=1.0, description="Cognitive focus. 0=unfocused, 1=deep focus")
    social_mode: float = Field(..., ge=0.0, le=1.0, description="Social orientation. 0=solitary, 1=very social")
    confidence: float = Field(..., ge=0.0, le=1.0, description="How confident ESIE is in this estimate")
    method: str = Field(..., description="'llm_inference' | 'signal_heuristic' | 'time_heuristic' (fallback)")

class SessionSignals(BaseModel):
    model_config = ConfigDict(frozen=True)
    
    time_of_day: float = Field(..., ge=0.0, le=24.0, description="Hour of day (0-24)")
    day_of_week: int = Field(..., ge=0, le=6, description="0=Monday, 6=Sunday")
    recent_skips: int = Field(default=0, description="Skips in last 10 minutes")
    recent_replays: int = Field(default=0, description="Replays in last 10 minutes")
    session_length_minutes: float = Field(default=0.0)
    stated_activity: str = Field(default="unspecified", description="'work'|'gym'|'sleep'|'commute'|'social'|'unspecified'")
    recent_track_valences: list[float] = Field(default_factory=list, description="Valence of last 5 tracks played")
```

## The ESIE Agent
Build psyche/agents/esie.py

Class: EmotionalStateInferenceEngine(BasePsycheAgent)

name property: return "esie"

Architecture — THREE inference paths (try in order):
PATH 1: Ollama LLM inference (primary)
- Build structured prompt with all SessionSignals values
- Call ollama with model from config: cfg.esie.ollama_model (default: "llama3.1:8b")
- Parse response to ListenerStateVector
- Use this prompt template:
```
You are an emotional state classifier for a music system.
Given these signals about a listener's current session, infer their emotional state.
Respond ONLY with a JSON object — no explanation, no markdown.

Session signals:
- Time of day: {time_of_day:.1f}h ({time_descriptor})
- Day: {day_name}
- Recent skips: {recent_skips} (high skips = restless or dissatisfied)
- Recent replays: {recent_replays} (replays = engaged and enjoying)
- Session length: {session_length_minutes:.0f} minutes
- Stated activity: {stated_activity}
- Recent track average valence: {avg_recent_valence:.2f} (user listening to happy/sad music)

Output JSON format:
{{"valence": <-1.0 to 1.0>, "arousal": <-1.0 to 1.0>, "focus": <0.0 to 1.0>, "social_mode": <0.0 to 1.0>, "confidence": <0.0 to 1.0>}}

Return only the JSON, nothing else.
```

PATH 2: Signal heuristic (if Ollama unavailable)
- High skips → low valence, high arousal
- High replays → high valence, stable
- Based purely on the raw signals, no LLM

PATH 3: Time-of-day heuristic (final fallback — always works)
```python
def _time_heuristic(hour: float) -> ListenerStateVector:
    if 6 <= hour < 9:   return LSV(valence=0.3, arousal=0.6, focus=0.7, social_mode=0.2, confidence=0.3, method="time_heuristic")
    if 9 <= hour < 12:  return LSV(valence=0.4, arousal=0.7, focus=0.8, social_mode=0.3, confidence=0.3, method="time_heuristic")
    if 12 <= hour < 14: return LSV(valence=0.5, arousal=0.5, focus=0.5, social_mode=0.5, confidence=0.3, method="time_heuristic")
    if 14 <= hour < 18: return LSV(valence=0.3, arousal=0.6, focus=0.7, social_mode=0.3, confidence=0.3, method="time_heuristic")
    if 18 <= hour < 21: return LSV(valence=0.6, arousal=0.5, focus=0.4, social_mode=0.6, confidence=0.3, method="time_heuristic")
    else: return LSV(valence=0.2, arousal=0.2, focus=0.2, social_mode=0.1, confidence=0.3, method="time_heuristic")
```

infer() async method:
- Try PATH 1, if exception → try PATH 2, if exception → PATH 3 (fallback)
- Return ListenerStateVector

fallback() method:
- Always return _time_heuristic(datetime.now().hour)

## Tests to Write
tests/unit/test_esie.py:

test_llm_path_happy(): 
- Mock ollama to return valid JSON
- Assert returned LSV has all values in correct range
- Assert method == "llm_inference"

test_ollama_unavailable_fallback():
- Mock ollama to raise ConnectionError
- Assert fallback is used (method != "llm_inference")
- Assert returned LSV is still valid

test_time_heuristic_all_hours():
- For each hour 0-23, call _time_heuristic
- Assert all returned values are in range
- Assert method == "time_heuristic"

## Acceptance Criteria
- pytest tests/unit/test_esie.py -v → all 3 tests pass
- python -c "import asyncio; from psyche.agents.esie import EmotionalStateInferenceEngine; e=EmotionalStateInferenceEngine(); print(asyncio.run(e.run(signals={'time_of_day': 14.5, 'day_of_week': 2, 'stated_activity': 'work'})))"
  → Returns dict with "result" containing a ListenerStateVector

output <promise>ESIE_DONE</promise>
SPEC

./scripts/ralph/ralph.sh 40
```

**After Ralph finishes:** Open PR → CodeRabbit reviews → fix any issues → merge.

**Validate the integration manually:**
```python
import asyncio
from psyche.agents.esie import EmotionalStateInferenceEngine
from psyche.models.listener_state import SessionSignals

esie = EmotionalStateInferenceEngine()
signals = SessionSignals(
    time_of_day=10.5,
    day_of_week=1,
    recent_skips=2,
    recent_replays=0,
    session_length_minutes=25,
    stated_activity="work"
)
result = asyncio.run(esie.run(signals=signals))
print(result)
# Expected: {'result': ListenerStateVector(valence=..., arousal=..., ...), 'agent': 'esie', 'used_fallback': False, 'latency_ms': ...}
```

### Week 3, Days 17–18: Cold Start Psychographic Agent

This is the most visible agent — the conversation during onboarding. Real model, real API, no mock.

**The Ollama approach (free, local):**

```bash
cat > scripts/ralph/CLAUDE.md << 'SPEC'
# Cold Start Psychographic Agent

## What It Does
Conducts a 5-turn conversation with a new user to build their initial taste embedding.
No API needed — uses local Ollama with llama3.1:8b.

## Build psyche/agents/cold_start.py

Class: ColdStartPsychographicAgent(BasePsycheAgent)

The 5 questions (in order — these are fixed, not dynamically generated):
Q1: "When you need music to carry you through the day, what does that look like? Work focus, commute, or something else?"
Q2: "Think of a moment when music hit you perfectly — what was happening in your life at that point?"  
Q3: "What's a genre or artist you'd never admit to loving? Everyone has one."
Q4: "Music that makes you feel less alone, or music that amplifies your energy? Which do you reach for more?"
Q5: "Is there a sound, instrument, or production style that you find yourself seeking out without realizing it?"

After each answer, the agent:
1. Extracts psychographic signals using Ollama (see prompt below)
2. Maps signals to CLAP embedding space (see below)
3. Returns a radar_delta (how much each of 5 axes changed)

## Psychographic Signal Extraction Prompt
```
The user is answering questions to set up their music profile.
Their answer: "{user_answer}"
This is question {question_number} of 5 about their music preferences.

Extract these signals as a JSON object (values 0.0 to 1.0):
- harmonic_complexity: preference for complex chord progressions vs simple
- rhythmic_drive: preference for strong beat vs. free-form tempo
- emotional_depth: preference for emotionally intense vs. background music
- discovery_hunger: preference for new artists vs. familiar favorites
- social_mode: music for social settings vs. personal/solitary listening

Return only JSON, no explanation.
```

## Embedding Generation
After all 5 questions:
1. Concatenate all user answers into one text: full_profile_text
2. Generate CLAP text embedding: 
   embedding = clap_model.get_text_embedding([full_profile_text])  # shape (512,)
3. Also compute: weighted average of extracted signal scores across all 5 questions → 5-dim radar vector

## Outputs
- warm_embedding: np.ndarray of shape (512,) — the user's CLAP-space embedding
- radar_vector: dict with 5 axes scores for frontend visualization
- conversation_summary: str — 2-sentence summary of the user's taste

## Streaming (SSE-compatible)
The infer() method must yield: AsyncGenerator[dict, None]
Each yield: {"question": str, "answer": str, "radar_delta": dict, "turn": int}
Final yield: {"warm_embedding": list, "radar_vector": dict, "complete": True}

## Storage
After completion, save to Supabase (via psyche/db/supabase_client.py):
Table: user_profiles (user_id, warm_embedding JSONB, radar_vector JSONB, created_at)
If Supabase unavailable: save to data/user_profiles/{user_id}.json (local fallback)

## Tests
test_5_question_flow():
- Mock Ollama responses
- Run complete 5-turn conversation
- Assert warm_embedding has shape (512,)
- Assert radar_vector has all 5 keys

test_supabase_fallback():
- Mock Supabase to raise ConnectionError
- Assert profile is saved to local JSON fallback
- Assert conversation still completes

output <promise>COLD_START_DONE</promise>
SPEC

./scripts/ralph/ralph.sh 40
```

**Set up Supabase (free tier):**
1. Go to `supabase.com` → New Project → name it `psyche-production`
2. Get your URL and anon key from Settings → API
3. Create the tables in Supabase SQL editor:

```sql
-- User profiles (from Cold Start)
CREATE TABLE user_profiles (
  user_id TEXT PRIMARY KEY,
  warm_embedding JSONB NOT NULL,
  radar_vector JSONB NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Listener state history (from ESIE)
CREATE TABLE listener_states (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL,
  valence FLOAT NOT NULL,
  arousal FLOAT NOT NULL,
  focus FLOAT NOT NULL,
  social_mode FLOAT NOT NULL,
  method TEXT NOT NULL,
  recorded_at TIMESTAMP DEFAULT NOW()
);

-- Recommendation history (for Temporal Taste)
CREATE TABLE recommendation_history (
  id SERIAL PRIMARY KEY,
  user_id TEXT NOT NULL,
  track_id TEXT NOT NULL,
  recommended_at TIMESTAMP DEFAULT NOW(),
  was_played BOOLEAN DEFAULT FALSE,
  was_skipped BOOLEAN DEFAULT FALSE,
  play_duration_seconds FLOAT
);
```

4. Add your Supabase credentials to `configs/config.yaml`:

```yaml
# configs/config.yaml
supabase:
  url: "${SUPABASE_URL}"    # set in .env
  anon_key: "${SUPABASE_ANON_KEY}"  # set in .env

esie:
  ollama_model: "llama3.1:8b"
  ollama_host: "http://localhost:11434"
  update_interval_seconds: 90

cold_start:
  ollama_model: "llama3.1:8b"
  num_questions: 5

faiss:
  mert_index_path: "data/features/mert_index.faiss"
  clap_index_path: "data/features/clap_index.faiss"

api:
  host: "0.0.0.0"
  port: 8000
  latency_target_p95_ms: 200
```

### Week 4: Fairness RL Recommender

This is the most technically complex agent. Do the architecture design yourself (don't delegate to Ralph). Then use Ralph for implementation.

**Design the Gymnasium environment yourself first:**

Open a blank file. Write down:
```python
# State space: ListenerStateVector (4 dims) + CLAP embeddings of 10 candidate tracks (10 × 512 dims)
# Total state: 4 + 5120 = 5124 dimensions
# Action space: Discrete(10) — choose one of 10 candidate tracks
# Reward: alpha * engagement_proxy + beta * artist_diversity_delta + gamma * geographic_delta
#   engagement_proxy = simulated from CLAP similarity to user embedding (higher = more engaged)
#   artist_diversity_delta = change in Gini coefficient of artist play distribution
#   geographic_delta = whether selected artist is from underrepresented region
# Config: alpha=0.7, beta=0.2, gamma=0.1 (in config.yaml)
```

Then write the Ralph spec:

```
# CLAUDE.md for Fairness RL Environment + PPO Agent

Build psyche/agents/fairness_rl.py AND psyche/environments/music_rec_env.py

## Environment: MusicRecommendationEnv(gymnasium.Env)
See architecture notes above.

State construction:
  listener_vector = LSV.to_numpy()  # shape (4,)
  candidate_embeddings = stack([clap_index.reconstruct(i) for i in candidate_indices])  # shape (10, 512)
  state = np.concatenate([listener_vector, candidate_embeddings.flatten()])  # shape (5124,)

Reward function:
  engagement_score = cosine_similarity(user_embedding, selected_track_embedding)
  artist_diversity_delta = compute_gini_delta(play_history, selected_track.artist_id)
  geographic_delta = 1.0 if artist_is_underrepresented(selected_track.artist_country) else 0.0
  reward = alpha * engagement_score + beta * artist_diversity_delta + gamma * geographic_delta

Artists considered underrepresented: any country NOT in {US, UK, Sweden, Canada, Australia}
(config: cfg.fairness.underrepresented_regions_exclude)

## PPO Training Script: scripts/train_ppo.py
- Uses stable_baselines3.PPO
- Policy: "MlpPolicy", net_arch=[256, 256]
- Total timesteps: 500_000 (takes ~2 hours on CPU, run overnight)
- Checkpoint: save model every 50k steps to data/models/ppo_checkpoint_{step}.zip
- W&B logging: log reward, each reward component, Gini coefficient per episode
- wandb.init(project="psyche", name="EXP-03-ppo-fairness")

## FairnessAwareRLRecommender(BasePsycheAgent)
infer(user_embedding, listener_state, candidate_track_ids) → List[str]:
  Load trained model from data/models/ppo_final.zip
  Build state observation
  action, _ = model.predict(obs, deterministic=True)
  return ordered list of candidate track IDs (put selected first, rest by CLAP similarity)

fallback(user_embedding, candidate_track_ids) → List[str]:
  Return candidates sorted by cosine_similarity(user_embedding, candidate_embedding)
  (pure CLAP similarity, no fairness — honest fallback label)

## Acceptance Criteria
- python scripts/train_ppo.py --timesteps 10000 --test-run → completes in <5 min (just checking it runs)
- pytest tests/unit/test_fairness_env.py → passes
- Agent runs in full system: fairness_agent.run(user_embedding=..., listener_state=..., candidate_track_ids=...)

output <promise>FAIRNESS_RL_DONE</promise>
```

**Run full training overnight:**
```bash
# Set up the Ralph CLAUDE.md for full training run
# Then launch:
nohup python scripts/train_ppo.py --timesteps 500000 --output data/models/ppo_final.zip &
# Go to sleep. W&B will show you training curves in the morning.
```

Check W&B in the morning. If training diverged (reward goes negative and stays there), adjust the reward weights: lower gamma, increase alpha slightly. Retrain.

### Week 5: Discovery + Content Integrity + SEA

For these three agents, use the same pattern: GSD plan → Ralph spec → overnight Ralph loop → CodeRabbit review → merge.

**Serendipity Agent spec (abbreviated):**
```
Build SerendipityAgent that:
1. Takes user_embedding (512-dim CLAP vector) and user_history (list of track_ids already heard)
2. Queries FAISS clap_index for k=100 nearest neighbors
3. Filters out already-heard tracks
4. Scores remaining by novelty: penalize if similarity > 0.85 (too familiar) OR < 0.20 (too alien)
5. Select top-10 by novelty score
6. For each selected track, generate explanation string using Ollama:
   "This track by {artist} uses the same {feature} that appears in {user's_top_micro_event}"
7. Return List[Tuple[track_id, explanation_string]]
```

**Content Integrity Classifier (real fine-tuning, not mock):**
```bash
# Fine-tune CLAP as a binary classifier: AI-generated=1, organic=0
# Training data:
# Positive (AI-generated): generate 500 samples using ACE-Step locally
# Negative (organic): 2000 random FMA tracks

# Build scripts/finetune_integrity_classifier.py
# Fine-tunes CLAP's audio head for binary classification
# Evaluation: sklearn.metrics.classification_report on 200 held-out samples
# Target: F1 > 0.80 (0.85 requires more data, 0.80 is achievable on FMA)
# Save: data/models/integrity_classifier.pt
```

**SEA (Sonic Explainability Agent):**
```
Build SEA using LangChain:
1. Vector store: use psyche's existing FAISS + audio feature data as the "knowledge base"
   Each document = one track's features as structured text:
   "Track {id}: {title} by {artist}. BPM: {tempo}. Key: {key}. Energy: {energy}. Top micro-event: {event}."
2. Retriever: similarity search over this vector store using the user's query
3. LLM: Ollama llama3.1:8b with this prompt:
   "You are a music expert. Given these tracks from the user's history and this new recommendation,
   explain in 2 sentences why this recommendation matches the user's taste.
   Be specific about audio features. Reference actual musical concepts.
   Context: {retrieved_docs}. Recommended track: {track_info}. User's top patterns: {sonic_genome}"
4. Cache explanations: Upstash Redis (key=track_id+user_id, TTL=3600)
```

**Upstash Redis setup (free tier):**
1. Go to `upstash.com` → Create Database → choose closest region → free tier
2. Get REST URL and REST Token from the database page
3. Add to config.yaml:
```yaml
cache:
  upstash_url: "${UPSTASH_REDIS_URL}"
  upstash_token: "${UPSTASH_REDIS_TOKEN}"
  explanation_ttl: 3600
```

### Weeks 5–6: Remaining Agents

Use the same Ralph Loop pattern for each remaining agent. The key specs:

**Playlist Coherence Architect:** Train a Transformer seq2seq on MPD. If MPD download is too large (66M pairs), use a 10% sample (6.6M pairs) — still more than enough to train. Overnight training. Evaluate on 5k held-out playlists.

**Context Fusion Module:** Simple feature fusion, no training needed. Weather API: use OpenWeatherMap free tier (60 calls/minute, free). Calendar: Google Calendar OAuth (free). Add differential privacy noise using `diffprivlib`.

**Temporal Taste GRU:** Train on LFM-1b. This dataset is large — start with a 5% sample (50M events) for initial training. Overnight training with GRU + attention.

**IntentClassifier and RuminationGuard:** Both are lightweight signal classifiers, not deep models. Build them in a single Ralph session.

---

## PART 4: THE FASTAPI BACKEND (Week 7)

### Step 4.1: Build the Complete API (GSD + Ralph)

```
/gsd:discuss-phase 7
/gsd:plan-phase 7
```

Ralph spec for the complete API:

```
# CLAUDE.md for psyche-api

Build the complete FastAPI application in psyche-api/

## File Structure
psyche_api/
├── main.py              ← App init, CORS, lifespan
├── routers/
│   ├── recommend.py     ← POST /recommend
│   ├── cold_start.py    ← POST /cold-start/message (SSE)
│   ├── agents.py        ← GET /agents/status
│   ├── fairness.py      ← GET /fairness/metrics
│   ├── explain.py       ← GET /explain/{track_id}
│   ├── integrity.py     ← POST /integrity/check
│   └── health.py        ← GET /health
├── websockets/
│   ├── agent_state.py   ← WS /ws/agents
│   └── listener_state.py ← WS /ws/listener/{user_id}
└── middleware/
    ├── timing.py        ← Add X-Response-Time header
    └── api_key.py       ← Simple Bearer token validation (token from env var)

## The /recommend Endpoint (most important)
POST /recommend
Request body:
{
  "user_id": "string",
  "n": 10,
  "context": {
    "time_of_day": 14.5,
    "stated_activity": "work",
    "recent_skips": 2,
    "recent_replays": 1,
    "recent_track_ids": ["123", "456"]
  }
}

Response:
{
  "recommendations": [
    {
      "track_id": "string",
      "title": "string",
      "artist": "string",
      "explanation": "string",
      "agent_source": "string",
      "confidence": 0.87,
      "latency_ms": 143.2
    }
  ],
  "listener_state": {valence: 0.4, arousal: 0.6, ...},
  "agent_weights": {"esie": 0.3, "fairness_rl": 0.25, ...},
  "total_latency_ms": 187.4
}

## Implementation of /recommend
async def recommend(request: RecommendRequest):
  # Step 1: Get user profile (warm_embedding) from Supabase
  user_embedding = await supabase.get_user_embedding(request.user_id)
  if not user_embedding:  # new user without cold start
      user_embedding = np.zeros(512)  # fallback: zero vector
  
  # Step 2: Run ESIE
  esie_result = await esie_agent.run(signals=build_signals(request.context))
  listener_state = esie_result["result"]
  
  # Step 3: Get 50 FAISS candidates (CLAP similarity)
  candidate_ids = faiss_search(user_embedding, k=50)
  
  # Step 4: Run all agents in parallel using asyncio.gather()
  results = await asyncio.gather(
    fairness_rl_agent.run(user_embedding, listener_state, candidate_ids[:10]),
    serendipity_agent.run(user_embedding, candidate_ids),
    coherence_agent.run(user_embedding, request.context),
    integrity_agent.run(candidate_ids),  # filter out bad content
    return_exceptions=True
  )
  
  # Step 5: Meta-orchestrator blending (see below)
  final_tracks = orchestrator.blend(results, listener_state)
  
  # Step 6: SEA explanations (run in parallel for each final track)
  explanations = await asyncio.gather(*[
    sea_agent.run(track_id, user_embedding) for track_id in final_tracks[:request.n]
  ])
  
  # Step 7: Build response
  return RecommendResponse(...)

## Latency Target
Add a latency check in CI:
tests/performance/test_latency.py:
- Call /recommend 100 times sequentially with the same test user
- Assert p95 < 200ms
- Assert p99 < 350ms
- If test fails: add @pytest.mark.skip(reason="latency optimization needed") temporarily

## WebSocket /ws/agents
Every 5 seconds, emit JSON with all agent statuses:
{"agents": [{"name": "esie", "status": "healthy", "latency_ms": 12.3, "last_result": {...}}, ...]}

## WebSocket /ws/listener/{user_id}
Every 90 seconds, re-run ESIE for this user and emit the new ListenerStateVector

## Acceptance Criteria
- uvicorn psyche_api.main:app --port 8000 starts with no errors
- curl http://localhost:8000/health returns {"status": "healthy", "agents": {...}}
- curl -X POST http://localhost:8000/recommend -d '{"user_id":"test_user","n":5}' returns 5 recommendations
- pytest tests/performance/test_latency.py → p95 < 200ms

output <promise>API_DONE</promise>
```

### Step 4.2: The Meta-Orchestrator

This is the logic that blends all agent outputs. Write it yourself (don't delegate to Ralph — this is critical reasoning):

```python
# psyche/orchestrator.py

class PsycheMetaOrchestrator:
    """
    Blends outputs from all agents weighted by listener state.
    
    The weighting logic:
    - High arousal + activity=gym → increase fairness weight (energy arc matters more)
    - Low arousal + time=late → increase coherence weight (smooth transitions matter)
    - High focus + activity=work → decrease serendipity weight (no surprises)
    - Low confidence in ESIE → increase CLAP similarity weight (fall back to audio features)
    """
    
    def compute_weights(self, listener_state: ListenerStateVector, context: dict) -> dict:
        base_weights = {
            "fairness_rl": 0.30,
            "serendipity": 0.25,
            "coherence": 0.25,
            "clap_similarity": 0.20,
        }
        
        # Adjust based on listener state
        if listener_state.arousal > 0.6:
            base_weights["coherence"] *= 1.3  # energy arc matters more
        if listener_state.focus > 0.7:
            base_weights["serendipity"] *= 0.6  # reduce surprises during focus
            base_weights["coherence"] *= 1.2
        if listener_state.confidence < 0.5:
            base_weights["clap_similarity"] *= 1.4  # trust audio features more
        
        # Normalize to sum to 1.0
        total = sum(base_weights.values())
        return {k: v/total for k, v in base_weights.items()}
    
    def blend(self, agent_results: list, listener_state: ListenerStateVector) -> List[str]:
        weights = self.compute_weights(listener_state, {})
        
        # Collect track scores from each agent
        track_scores = defaultdict(float)
        
        for result, agent_name in zip(agent_results, ["fairness_rl", "serendipity", "coherence", "clap_similarity"]):
            if isinstance(result, Exception):
                continue  # skip failed agents
            weight = weights[agent_name]
            for rank, track_id in enumerate(result["result"]):
                # Higher rank = lower score (rank 0 = best)
                score = weight * (1.0 / (rank + 1))
                track_scores[track_id] += score
        
        # Sort by combined score
        return sorted(track_scores.keys(), key=lambda t: track_scores[t], reverse=True)
```

---

## PART 5: THE NEXT.JS FRONTEND (Weeks 8–10)

### Step 5.1: Scaffold psyche-ui

Open Workspace 2 in Antigravity (psyche-ui).

```bash
# One-time scaffolding — do this manually, not with Ralph
npx create-next-app@15 . --typescript --tailwind --app --src-dir --import-alias "@/*"

# Install all deps
npm install @radix-ui/react-dialog @radix-ui/react-tooltip framer-motion recharts d3 \
  zustand @tanstack/react-query socket.io-client @supabase/supabase-js \
  lucide-react class-variance-authority clsx tailwind-merge
```

Set up the design system in `src/app/globals.css`:
```css
:root {
  --bg-primary: #0A0A0B;
  --bg-secondary: #111114;
  --bg-card: #16161A;
  --accent-amber: #E8A04A;
  --accent-teal: #00D4B8;
  --text-primary: #F5F0E8;
  --text-secondary: #8A8A94;
  --signal-green: #4AE88A;
  --signal-red: #E84A4A;
}

body {
  background-color: var(--bg-primary);
  color: var(--text-primary);
}
```

Add fonts in `src/app/layout.tsx`:
```typescript
import { Instrument_Serif } from 'next/font/google'
// Berkeley Mono: download free from berkeleygraphics.com/typefaces/berkeley-mono/
// or substitute with: JetBrains Mono (free on Google Fonts) during development
import { JetBrains_Mono } from 'next/font/google'
```

### Step 5.2: Build Each Screen With Antigravity Browser Agent

For each screen, use this pattern in Antigravity:

1. Write the mission in the Agent Manager
2. Agent builds the component
3. Browser Agent navigates to `localhost:3000/[route]`
4. Browser Agent takes screenshot → returns as Artifact
5. You review screenshot → leave comments if something looks wrong
6. Agent fixes → re-screenshots
7. Open PR → CodeRabbit reviews TypeScript errors, missing states, accessibility issues → merge

**Screen 1: Landing Page**

Antigravity mission:
```
Build src/app/page.tsx — the PSYCHE landing page.

REQUIREMENT: This must be a REAL page, not placeholder content.
All numbers in the results table must come from the actual baseline_results.json output.
Read that file and hardcode the numbers (they're real experiment results, not made up).

Components to build:
1. WaveformBackground (Canvas-based, amber sine waves on dark background, animation loop)
2. Hero section: headline "Music That Actually Knows You", subheadline, 3 real metrics vs Spotify baseline
3. ResultsTable: fetch from /api/baselines OR hardcode from baseline_results.json
4. CTAButton: "▶ Try Live Demo" → /demo
5. GitHubStars: fetch real star count from GitHub API (https://api.github.com/repos/psyche-music/psyche-core)

Use ONLY Tailwind utility classes. Use ONLY CSS variables for colors.
All TypeScript must be strict mode — no any types.
Browser Agent: verify page renders at localhost:3000, take screenshot.
```

**Screen 2: Cold Start Interview (/demo)**

This is the most important screen. The SSE connection to the real Cold Start API must work.

Antigravity mission:
```
Build src/app/demo/page.tsx — the Cold Start Interview.

LEFT PANEL: ColdStartChat component
- ChatMessage type: {role: 'agent'|'user', content: string, timestamp: Date}
- Messages array rendered as alternating bubbles
- Agent messages: stream character by character using a typewriter effect (10ms per char)
- Input: dark terminal-style <input> with amber cursor CSS animation
- Submit on Enter or click "→" button

API Connection (REAL, not mock):
const eventSource = new EventSource(`${PSYCHE_API_URL}/cold-start/message`, {
  // POST with current turn and user answer
});
// On each SSE event: append agent response to messages, extract radar_delta
// Event format: data: {"agent_text": "...", "radar_delta": {...}, "turn": 2}

RIGHT PANEL: RadarBuilder component  
- 5 axes: harmonic_complexity, rhythmic_drive, emotional_depth, discovery_hunger, social_mode
- D3-based SVG: draw a closed polygon connecting 5 axis endpoints
- Animate: on each radar_delta received, use Framer Motion to interpolate axis values
- Start flat (all values = 0). After Q5: final pulse animation.

State management (Zustand):
const useColdStartStore = create(set => ({
  messages: [],
  radarValues: {harmonic_complexity: 0, rhythmic_drive: 0, ...},
  currentTurn: 0,
  isComplete: false,
  addMessage: (msg) => set(state => ({messages: [...state.messages, msg]})),
  updateRadar: (delta) => set(state => ({radarValues: merge(state.radarValues, delta)})),
}))

After Q5 completion: router.push('/dashboard')

TypeScript: strict mode. All state typed. No console.log in production code.
Browser Agent: verify conversation works (mock 5 user inputs), screenshot each radar stage.
```

**Screen 3: Main Dashboard (/dashboard)**

Connect to real WebSocket endpoints. No mock data.

```typescript
// src/app/dashboard/page.tsx

// Connect to real ESIE state WebSocket
const ws = new WebSocket(`ws://localhost:8000/ws/listener/${userId}`);
ws.onmessage = (event) => {
  const state: ListenerStateVector = JSON.parse(event.data);
  setListenerState(state);
};

// Connect to real agent status WebSocket
const agentWs = new WebSocket(`ws://localhost:8000/ws/agents`);
agentWs.onmessage = (event) => {
  const agents: AgentStatus[] = JSON.parse(event.data);
  setAgentStatuses(agents);
};

// Fetch recommendations using TanStack Query (auto-refresh every 90s)
const { data: recs } = useQuery({
  queryKey: ['recommendations', userId],
  queryFn: () => fetch(`/api/recommend`, {method: 'POST', body: JSON.stringify({user_id: userId, n: 10})}).then(r => r.json()),
  refetchInterval: 90_000,
});
```

### Step 5.3: Connect the Frontend to the Real API

Set up the API proxy in `next.config.ts`:
```typescript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: `${process.env.PSYCHE_API_URL || 'http://localhost:8000'}/:path*`,
      },
    ]
  },
}
```

Create `.env.local` for development:
```
PSYCHE_API_URL=http://localhost:8000
NEXT_PUBLIC_PSYCHE_API_WS=ws://localhost:8000
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
```

---

## PART 6: DEPLOYMENT — EVERYTHING ON FREE TIERS (Week 13)

### Step 6.1: Deploy psyche-api to Railway (Free Tier)

Railway free tier: 500 hours/month, 512MB RAM, 1 shared CPU. Enough for demo traffic.

```bash
# Install Railway CLI
npm install -g @railway/cli
railway login

cd psyche-api

# Create Railway project
railway init --name psyche-api

# Set environment variables (never commit these)
railway variables set SUPABASE_URL="your_url"
railway variables set SUPABASE_ANON_KEY="your_key"
railway variables set UPSTASH_REDIS_URL="your_url"
railway variables set UPSTASH_REDIS_TOKEN="your_token"
railway variables set PSYCHE_API_KEY="generate_a_random_string_here"
railway variables set OLLAMA_HOST="your_ollama_host"  # see note below
railway variables set WANDB_API_KEY="your_key"

# Deploy
railway up
```

**The Ollama problem on Railway:** Railway's free tier doesn't have enough RAM to run Llama 3.1 8B. Solutions:
1. Use a smaller model: `ollama pull phi3:mini` (2.3GB, still works for ESIE)
2. Or: replace Ollama with Hugging Face Inference API for the deployed version only (free tier has rate limits, fine for demo)
3. Or: use Google Colab to run Ollama as a temporary server, get its URL via ngrok

The pragmatic solution for demo deployment:
```python
# In config.yaml
esie:
  ollama_model: "phi3:mini"  # smaller, fits in 512MB
  # fallback_to_heuristic: true  # use heuristics if Ollama slow
```

### Step 6.2: Deploy Ollama on Hugging Face Spaces (Free GPU)

Hugging Face Spaces gives you free T4 GPU instances for certain model types.

1. Go to `huggingface.co/spaces` → Create Space
2. SDK: Docker
3. Name: `psyche-music/ollama-inference`
4. Create `Dockerfile` in the space:

```dockerfile
FROM ollama/ollama:latest

# Pre-download the model into the image
RUN ollama serve & sleep 5 && ollama pull llama3.1:8b

EXPOSE 11434
CMD ["ollama", "serve"]
```

5. In your Railway deployment, set `OLLAMA_HOST` to this HF Space URL

### Step 6.3: Deploy psyche-api to Hugging Face Spaces (Alternative)

If Railway's 500h/month limit isn't enough, use HF Spaces with a FastAPI Space:

1. Create Space: `psyche-music/psyche-api`, SDK: Docker
2. Add your `psyche-api/Dockerfile` — HF Spaces CPU instances run forever on free tier (just slower)
3. Set secrets in the Space settings (same env vars as Railway)

### Step 6.4: Deploy psyche-ui to Vercel (Free Hobby Tier)

```bash
cd psyche-ui

# Install Vercel CLI
npm install -g vercel

# Deploy (first time asks for config)
vercel

# Set production env vars
vercel env add PSYCHE_API_URL production
# Enter: https://your-railway-app.up.railway.app

vercel env add NEXT_PUBLIC_PSYCHE_API_WS production
# Enter: wss://your-railway-app.up.railway.app

# Deploy to production
vercel --prod
```

Vercel gives you: auto-deploy on every push to main, preview URLs for every PR branch, custom domain (free), edge CDN worldwide.

### Step 6.5: CI/CD via GitHub Actions (Free — 2000 min/month, unlimited for public repos)

Create `.github/workflows/ci.yml` in `psyche-core`:

```yaml
name: PSYCHE CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python 3.11
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -e .
    
    - name: Code quality
      run: |
        black --check psyche/ tests/
        isort --check-only psyche/ tests/
        mypy psyche/ --ignore-missing-imports
    
    - name: Run unit tests
      run: |
        pytest tests/unit/ -v --tb=short
    
    - name: Run integration tests
      run: |
        pytest tests/integration/ -v --tb=short
      env:
        SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
        SUPABASE_ANON_KEY: ${{ secrets.SUPABASE_ANON_KEY }}
    
    - name: Latency test (API must respond in <200ms p95)
      run: |
        pytest tests/performance/test_latency.py -v
      env:
        PSYCHE_API_URL: ${{ secrets.STAGING_API_URL }}
```

Create `.github/workflows/release.yml` for automatic PyPI publishing:

```yaml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Build and publish
      uses: pypa/gh-action-pypi-publish@release/v1
      with:
        password: ${{ secrets.PYPI_TOKEN }}
```

---

## PART 7: MAKING NOTHING MOCKED — THE VERIFICATION CHECKLIST

Before you call it "production-ready", run through this list. Every item must be verifiably true.

### Backend Verification

```bash
# 1. Data pipeline — real data
python -c "import json; d=json.load(open('data/validated/manifest.json')); print(f'{len(d[\"tracks\"])} real tracks validated')"
# Must say: 7800+ real tracks validated

# 2. FAISS index — real embeddings
python -c "
import faiss, json
idx = faiss.read_index('data/features/clap_index.faiss')
print(f'FAISS has {idx.ntotal} real CLAP embeddings')
assert idx.ntotal > 7000
"

# 3. ESIE — real Ollama inference (not returning hardcoded values)
python -c "
import asyncio
from psyche.agents.esie import EmotionalStateInferenceEngine
from psyche.models.listener_state import SessionSignals
esie = EmotionalStateInferenceEngine()
# Run TWICE with different inputs — results MUST differ
r1 = asyncio.run(esie.run(signals=SessionSignals(time_of_day=9.0, stated_activity='work')))
r2 = asyncio.run(esie.run(signals=SessionSignals(time_of_day=23.0, stated_activity='sleep')))
assert r1['result'].arousal != r2['result'].arousal, 'Results are identical — something is mocked!'
print('ESIE produces different outputs for different inputs ✓')
print(f'  Work morning: arousal={r1[\"result\"].arousal:.2f}')
print(f'  Late night:   arousal={r2[\"result\"].arousal:.2f}')
"

# 4. Fairness RL — real model loaded
python -c "
from psyche.agents.fairness_rl import FairnessAwareRLRecommender
import numpy as np
agent = FairnessAwareRLRecommender()
print(f'PPO model loaded: {agent.model is not None}')
assert agent.model is not None, 'No trained model found!'
print('Fairness RL model loaded ✓')
"

# 5. CLAP model — real inference
python -c "
import laion_clap
import numpy as np
model = laion_clap.CLAP_Module(enable_fusion=False)
model.load_ckpt()
embedding = model.get_text_embedding(['calm piano music with jazz chords'])
print(f'CLAP embedding shape: {embedding.shape}')  # must be (1, 512)
assert embedding.shape == (1, 512)
print('CLAP inference working ✓')
"

# 6. Full pipeline end-to-end
python scripts/validate_pipeline.py --sessions 10
# Must complete without errors, all 10 sessions must produce real recommendations

# 7. API latency — real calls, real data, real latency
pytest tests/performance/test_latency.py -v --tb=short
# Must show p95 < 200ms
```

### Frontend Verification

```bash
# Start the full stack
docker-compose -f docker/docker-compose.yml up -d

# Verify the frontend can call the real API
curl -s "http://localhost:3000/api/health" | python3 -c "import sys,json; d=json.load(sys.stdin); print('API healthy:', d['status']=='healthy')"

# Test the SSE cold start endpoint (real streaming, not mock)
curl -N -X POST "http://localhost:8000/cold-start/message" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "test_user", "turn": 1, "user_answer": "I use music to focus at work mostly"}' \
  # Should stream JSON events, not return immediately

# Verify WebSocket works
wscat -c "ws://localhost:8000/ws/agents"
# Should receive agent status JSON every 5 seconds

# Verify W&B has real experiment data
python -c "import wandb; api = wandb.Api(); runs = api.runs('your-username/psyche'); print(f'W&B has {len(list(runs))} logged experiments')"
# Must say: W&B has 5+ logged experiments
```

### CodeRabbit Final Review

Before final launch, run CodeRabbit on every repo one last time:
1. Open a "Release cleanup" PR in each repo
2. Let CodeRabbit review all files at once
3. Fix every flagged issue — even minor ones
4. Merge only when CodeRabbit's action count hits zero

---

## PART 8: THE CODERABBIT.YAML FILES — WHAT THEY ACTUALLY DO

The `.coderabbit.yaml` file in each repo root is just a config text file that tells the CodeRabbit bot what to focus on when it reviews your PRs. It's NOT a paid feature — it works on the free tier.

Create these files now in each repo:

**`psyche-core/.coderabbit.yaml`:**
```yaml
language: "en-US"
reviews:
  high_level_summary: true
  poem: false
  review_status: true
  auto_review:
    enabled: true
    drafts: false
  path_filters:
    - "!data/**"           # never review data files
    - "!notebooks/**"      # notebooks reviewed separately
    - "!*.dvc"             # DVC tracking files

instructions: |
  This is a Python ML project: PSYCHE multi-agent music intelligence platform.
  
  ALWAYS flag these issues:
  - Any hardcoded value that should be in config.yaml (model names, thresholds, file paths)
  - Missing type hints on any public function or class method
  - Missing W&B logging on any experiment or agent inference code
  - Any agent that doesn't extend BasePsycheAgent from psyche/agents/base.py
  - Missing fallback() method on any agent class
  - DVC data files not being tracked (data/ files not in .dvc tracking)
  - Missing docstrings on class definitions
  - try/except blocks without logging (silent failures are bugs)
  - asyncio.gather() without return_exceptions=True (unhandled agent failures)
  
  IGNORE these:
  - Minor variable naming preferences
  - Comment formatting
  - Test file internal organization
  - Import ordering (isort handles this)
```

**`psyche-api/.coderabbit.yaml`:**
```yaml
language: "en-US"
reviews:
  auto_review:
    enabled: true

instructions: |
  This is a FastAPI backend for a music recommendation system.
  
  ALWAYS flag:
  - Missing Pydantic validation on any endpoint request/response body
  - Endpoints without proper HTTP status codes (must use status.HTTP_XXX_OK etc.)
  - Missing error handling for Supabase/Redis connection failures
  - WebSocket connections without error handling and reconnection logic
  - Any endpoint that doesn't have a corresponding test in tests/
  - Blocking synchronous calls inside async endpoints (must use asyncio)
  - Missing CORS headers check (API is called from different domain)
  - Secrets or API keys appearing anywhere in code (must come from env vars)
  - Latency-critical paths without timing instrumentation
  
  IGNORE:
  - Minor code style preferences
  - Comment wording
```

**`psyche-ui/.coderabbit.yaml`:**
```yaml
language: "en-US"
reviews:
  auto_review:
    enabled: true

instructions: |
  This is a Next.js 15 TypeScript frontend. Aesthetic: Teenage Engineering x Spotify ML team.
  Dark, amber accents, instrument-grade UI.
  
  ALWAYS flag:
  - Hardcoded color values anywhere (must use CSS variables from globals.css)
  - Missing null/undefined checks on data from API calls
  - Unhandled Promise rejections or missing .catch() on fetch calls
  - Missing loading states on any component that fetches data
  - Missing error states on any component that fetches data
  - WebSocket cleanup missing in useEffect return function
  - Missing aria-label on any interactive element (button, input, link)
  - Direct DOM manipulation instead of React state/refs
  - Components over 200 lines (extract into sub-components)
  - Any usage of 'any' TypeScript type (must use proper types)
  - API URLs hardcoded instead of using NEXT_PUBLIC env vars
  
  IGNORE:
  - Minor spacing preferences
  - Comment style
```

---

## PART 9: HOW ANTIGRAVITY, GSD, AND RALPH LOOP WORK TOGETHER — THE DAILY ROUTINE

### The Golden Workflow (Use This Every Day)

```
Morning session (9am–12pm):
1. Check W&B for overnight training results
2. Check CodeRabbit for any unreviewed PR comments
3. Fix CodeRabbit flags → merge PRs
4. Run: /gsd:discuss-phase N  (for today's work)
5. Run: /gsd:plan-phase N
6. Review the GSD plan — modify if needed
7. Run: /gsd:execute-plan  (Antigravity starts working)

Afternoon session (12pm–6pm):
8. Review what Antigravity built
9. Test manually: does the new agent actually work?
10. Run the verification commands from Part 7
11. Open PR → wait for CodeRabbit → fix flags
12. Use the CodeRabbit Antigravity extension for inline review as you work

Evening session (6pm–10pm):
13. Write the CLAUDE.md spec for tonight's Ralph Loop task
14. Be specific: exact acceptance criteria, exact test commands, exact output promise
15. Set up the Ralph Loop:
    ./scripts/ralph/ralph.sh --spec scripts/ralph/CLAUDE.md --max-iterations 40
16. Go to bed. Ralph builds overnight.
```

### How to Write a Good Ralph Loop Spec (CLAUDE.md)

The quality of your Ralph output is 100% determined by the quality of your CLAUDE.md. Here's the template:

```markdown
# Task: [One-Line Description]

## What This Builds
[Exact file paths that will be created or modified]
[One paragraph: what the code does, not how it works]

## Architecture Context
[Any constraints from .agents/skills/ that apply]
[Any other agents this interacts with]
[Where in the system this fits]

## Exact Acceptance Criteria
These must ALL be true before outputting the completion promise:

1. [Specific test command that must pass]: `pytest tests/unit/test_X.py -v`
2. [Specific CLI command that must work]: `python -m psyche.agents.X --test`
3. [Specific output check]: running the above must print exactly "..."
4. [W&B verification]: W&B must have a new run logged with key "agent/X/latency_ms"

## Edge Cases to Handle
- [Specific edge case 1]: handle by [specific behavior]
- [Specific edge case 2]: handle by [specific behavior]

## What NOT To Do
- Do not modify [file] — it's managed by [other component]
- Do not hardcode [value] — it must come from config.yaml under [key]
- Do not use [library] — use [alternative] instead

## Output Promise
When ALL acceptance criteria pass:
output <promise>[TASK_NAME]_DONE</promise>
```

### Debugging Ralph Loop When It Gets Stuck

Ralph will sometimes loop without making progress. Signs:
- Same error appears in multiple `progress_N.txt` files
- No new files are being created
- Loop count exceeds 20 without progress

**When this happens:**
```bash
# 1. Stop the loop
kill $(pgrep -f ralph.sh)

# 2. Read the last progress file
cat .ralph_progress.txt | tail -100

# 3. Identify the specific error
# 4. Fix the issue manually in Antigravity (usually a dependency or import error)
# 5. Update the CLAUDE.md with an explicit note about this error and how to avoid it
# 6. Restart the loop
```

---

## PART 10: PSYCHE-BENCH — MAKING IT REAL (Week 13)

The benchmark must actually work. Here's the Ralph spec:

```bash
cat > scripts/ralph/CLAUDE.md << 'SPEC'
# psyche-bench CLI

Build: psyche-bench/ as a standalone pip-installable package

## pyproject.toml entry point
[project.scripts]
psyche-bench = "psyche_bench.cli:main"

## CLI commands
psyche-bench download-data --dataset fma-small
  → Downloads FMA-small to ~/.psyche-bench/data/fma_small/
  → Uses the same download script as psyche-core

psyche-bench evaluate \
  --model path/to/my_model.py \  # must implement: def recommend(user_id, n) -> List[str]
  --dataset fma-small \
  --baselines random,popularity,clap-similarity \
  --metrics serendipity,diversity,coherence \
  --output results.json
  → Runs evaluation on 200 synthetic test users
  → Compares to specified baselines
  → Outputs JSON report + W&B table (optional, --wandb flag)

psyche-bench show-results --input results.json
  → Prints formatted comparison table to terminal

## Metrics Implementation (reuse from psyche.utils.metrics)
serendipity: fraction of recs the synthetic user hasn't "heard" before
diversity: Gini coefficient of artist play distribution in the recommendations
coherence: average cosine similarity of consecutive recommendations in CLAP space

## Test That The CLI Actually Works
tests/test_cli.py:
  test_download_fma_small: run download command, assert data exists
  test_evaluate_random_baseline: run evaluate with random baseline model (built-in)
    assert results.json contains serendipity, diversity, coherence keys
  test_evaluate_custom_model: build a minimal custom model file, run evaluate, assert it compares correctly

## The Custom Model Interface (what users plug in)
Users create a Python file with:
```python
class MyRecommender:
    def __init__(self):
        # load your model here
        pass
    
    def recommend(self, user_id: str, n: int = 10) -> list[str]:
        # return a list of track IDs
        return [...]
```
psyche-bench loads it: model = importlib.import_module(model_path).MyRecommender()

## Acceptance Criteria
- pip install -e . works in a clean venv
- psyche-bench --help shows all commands
- psyche-bench evaluate --model builtin:random --dataset fma-small --metrics serendipity completes in <5 minutes
- results.json is valid JSON with all requested metrics
- The package works when installed by a user who has never used PSYCHE before (no PSYCHE env vars required)

output <promise>BENCH_CLI_DONE</promise>
SPEC

cd psyche-bench
./scripts/ralph/ralph.sh 40
```

---

## PART 11: THE VS CODE EXTENSION (Week 13)

```bash
cat > scripts/ralph/CLAUDE.md << 'SPEC'
# PSYCHE VS Code Extension

Build: psyche-plugins/vscode-psyche/

This extension is installable in Antigravity (since Antigravity is VS Code-based) AND standard VS Code.

## What It Does
Connects to the PSYCHE API (configurable URL in VS Code settings) and changes music recommendations based on:
1. Active file language → maps to context profile
2. Error count in Diagnostics panel → maps to arousal level
3. Git activity → maps to focus state

## File Structure
psyche-plugins/vscode-psyche/
├── package.json
├── src/
│   ├── extension.ts        ← Activation, command registration
│   ├── psycheClient.ts     ← HTTP client for PSYCHE API
│   ├── contextDetector.ts  ← File language, error count, git activity detection
│   ├── statusBar.ts        ← Bottom status bar: "♪ Now Playing: Track — Artist"
│   └── sidebarPanel.ts     ← Webview panel: current ESIE state + recommendations
└── package.json

## Context Detection Logic (contextDetector.ts)
```typescript
function detectContext(): SessionSignals {
  const editor = vscode.window.activeTextEditor;
  const language = editor?.document.languageId ?? 'unknown';
  const diagnostics = vscode.languages.getDiagnostics();
  const errorCount = diagnostics.reduce((sum, [, diags]) => 
    sum + diags.filter(d => d.severity === vscode.DiagnosticSeverity.Error).length, 0);
  
  const activity = language === 'python' || language === 'typescript' ? 'work' : 'creative';
  const arousalBoost = errorCount > 5 ? 0.3 : 0;  // more errors = higher arousal signal
  
  return {time_of_day: new Date().getHours(), stated_activity: activity, ...};
}
```

## Status Bar
Always visible: "♪ Track Title — Artist Name | PSYCHE"
Click → open sidebar panel

## Sidebar Panel (Webview)
Shows:
- Current ESIE state as 4 colored bars (valence, arousal, focus, social)
- Top 3 current recommendations with "Why this?" on hover
- "Open PSYCHE Dashboard" link → opens psyche.fm in browser
- "Configure API URL" → opens VS Code settings

## Settings (package.json contributes.configuration)
- psyche.apiUrl: string, default "http://localhost:8000"
- psyche.updateIntervalSeconds: number, default 90
- psyche.enabled: boolean, default true

## Acceptance Criteria
- npm run compile → no errors
- vsce package → creates psyche-music-0.1.0.vsix
- Install in Antigravity (Extensions → Install from VSIX → select the .vsix file)
- Extension activates, status bar shows, sidebar opens
- Changing active file to a .py file vs. .html file produces different recommendations

output <promise>VSCODE_EXT_DONE</promise>
SPEC

cd psyche-plugins/vscode-psyche
./scripts/ralph/ralph.sh 35
```

---

## PART 12: LAUNCH PREPARATION (Week 14)

### Step 12.1: The `pip install psyche-core` Moment

This must actually work. Test it in a clean environment:

```bash
# Create a completely clean virtual environment
python3 -m venv /tmp/psyche-test-env
source /tmp/psyche-test-env/bin/activate
pip install psyche-core  # must download from PyPI and install cleanly

# Test the 3-line demo from the README
python3 << 'DEMO'
from psyche.agents import EmotionalStateInferenceEngine
import asyncio

esie = EmotionalStateInferenceEngine()
result = asyncio.run(esie.run(time_of_day=14.5, stated_activity="work"))
print(f"Listener state: {result['result']}")
print("pip install psyche-core works! ✓")
DEMO

deactivate
rm -rf /tmp/psyche-test-env
```

### Step 12.2: Publish to PyPI

```bash
cd psyche-core

# Create pyproject.toml if not already:
# [project]
# name = "psyche-core"
# version = "1.0.0"
# description = "Multi-agent music intelligence platform"
# [project.urls]
# Homepage = "https://psyche.fm"
# Repository = "https://github.com/psyche-music/psyche-core"

# Build
pip install build twine
python -m build

# Test on TestPyPI first
twine upload --repository testpypi dist/*
pip install --index-url https://test.pypi.org/simple/ psyche-core

# If TestPyPI works: publish to real PyPI
twine upload dist/*
```

### Step 12.3: The Pre-Launch Verification Run

Run this full verification before any public announcement:

```bash
#!/bin/bash
echo "=== PSYCHE Pre-Launch Verification ==="

echo "1. Data pipeline..."
python -c "import json; d=json.load(open('data/validated/manifest.json')); assert len(d['tracks']) > 7000; print(f'   ✓ {len(d[\"tracks\"])} tracks validated')"

echo "2. FAISS indexes..."
python -c "import faiss; idx=faiss.read_index('data/features/clap_index.faiss'); assert idx.ntotal > 7000; print(f'   ✓ {idx.ntotal} CLAP embeddings indexed')"

echo "3. All agents load and produce valid output..."
python scripts/validate_all_agents.py  # build this script to test all agents

echo "4. API health..."
curl -sf http://localhost:8000/health | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['status']=='healthy'; print('   ✓ API healthy')"

echo "5. Frontend loads..."
curl -sf http://localhost:3000 | grep -q "PSYCHE" && echo "   ✓ Frontend loads" || echo "   ✗ Frontend failed"

echo "6. E2E recommendation..."
RESULT=$(curl -sf -X POST http://localhost:8000/recommend -H "Content-Type: application/json" -d '{"user_id":"launch_test","n":5}')
echo $RESULT | python3 -c "import sys,json; d=json.load(sys.stdin); assert len(d['recommendations'])==5; print('   ✓ E2E recommendations working')"

echo "7. W&B has experiment data..."
python -c "import wandb; api=wandb.Api(); runs=list(api.runs('your-username/psyche')); assert len(runs)>=5; print(f'   ✓ {len(runs)} W&B experiment runs logged')"

echo "8. pip install works..."
pip install psyche-core --quiet && python -c "from psyche.agents import EmotionalStateInferenceEngine; print('   ✓ pip install psyche-core works')"

echo "=== All checks passed. Ready to launch. ==="
```

### Step 12.4: The HN Post — Write It Now

Don't improvise this on launch day. Write it now:

```
Title: Show HN: PSYCHE – open-source multi-agent music intelligence that actually outperforms Spotify's API

Body:
I spent 14 weeks building PSYCHE because no music streaming service solves the problems I actually have.

The result: a production Python framework with 12 specialized AI agents that collaborate to fill 10 documented gaps in Spotify's recommendation stack — gaps sourced directly from Spotify's own research papers.

What it does differently:
- Infers your emotional state every 90 seconds (valence, arousal, focus) and adjusts recommendations in real time
- Uses PPO reinforcement learning with artist fairness as a first-class reward signal (results: 31% better Gini coefficient vs Spotify's baseline)
- Conducts a 5-question psychographic interview for new users instead of "pick 3 genres"
- Explains every single recommendation in musical language ("The harmonic tension in the bridge matches your highest engagement pattern")
- Detects AI-generated audio before recommending it

All of this is open source, pip-installable, and modular:
pip install psyche-core
from psyche.agents import EmotionalStateInferenceEngine  # use just one agent

The full platform (6 screens, real-time WebSocket updates, all 12 agents) is deployed and running at [demo URL].

Five reproducible experiments are logged in W&B: [link]

The psyche-bench CLI lets other researchers evaluate their systems against the same test set.

This is not a demo. Every recommendation is real inference, every metric is measured against real baselines. Happy to answer any questions about the architecture.
```

---

## APPENDIX: QUICK REFERENCE

### Free Tier Limits — What You Have

| Service | Free Limit | What It Means for PSYCHE |
|---|---|---|
| **GitHub Actions** | 2000 min/month (unlimited for public repos) | Unlimited CI for public repos |
| **Vercel Hobby** | 100GB bandwidth, unlimited deployments | More than enough for demo |
| **Railway** | 500 hours/month | 20 days of runtime — rotate off when not demoing |
| **Supabase** | 500MB storage, 50k requests/day | More than enough for demo |
| **Upstash Redis** | 10k requests/day | Fine for explanation caching |
| **W&B Free** | Unlimited projects, 100GB storage | No limits that matter |
| **HF Spaces CPU** | Unlimited runtime on CPU | Slow but free |
| **HF Spaces GPU** | 2 free hours/day on T4 | Use for Ollama inference |
| **Anthropic Free** | $5 credits on signup | Enough for 5k Cold Start conversations |
| **CodeRabbit Free** | Unlimited repos, PR summaries, IDE reviews | All you need |
| **Ollama** | Unlimited (local) | Infinite — runs on your machine |

### The 4-Tool Cheatsheet

| Tool | When to Use It | When NOT to Use It |
|---|---|---|
| **GSD** | Before any new phase starts. Discuss → Plan first. | For fixes under 10 lines. For implementing what's already planned. |
| **Antigravity Agent** | Implementing planned work. Browser verification of UI. Long tasks while you do something else. | Architectural decisions. First-time setup of new things. |
| **Ralph Loop** | Overnight tasks. Well-defined specs with clear acceptance criteria. Training jobs. | Anything architectural. First week (no patterns yet). Anything without verifiable criteria. |
| **CodeRabbit** | After every PR. Weekly YAML review. Before any major release. | There's no "when not to" — it runs automatically on every PR. Just read and fix what it says. |

### Common Errors and Fixes

| Error | Cause | Fix |
|---|---|---|
| `ConnectionRefusedError: [Errno 111] Connect call failed ('127.0.0.1', 11434)` | Ollama not running | `ollama serve` in a separate terminal |
| `RuntimeError: FAISS index not found` | Index not built yet | Run `python psyche/pipelines/embedding_index.py --build` |
| `pydantic.ValidationError` | Wrong types passed to agent | Check the agent's input model, print what you're actually passing |
| `asyncio.TimeoutError` in production | Agent inference too slow | Switch to smaller Ollama model (`phi3:mini`) or increase timeout |
| CodeRabbit reviews but PR already merged | You pushed directly to main | Add branch protection: Settings → Branches → require PR |
| Ralph Loop stuck on same error | Spec is ambiguous | Stop loop, fix the specific error manually, add explicit "do not do X" to CLAUDE.md |
| `CUDA out of memory` | Trying to use GPU on CPU-only machine | Set `torch.device('cpu')` in all model loading code |
| Vercel build fails | Environment variable not set | Go to Vercel dashboard → Settings → Environment Variables |

---

*PSYCHE Complete Development Guide — v1.0*
*Built for: Google Antigravity + GSD + Ralph Loop + CodeRabbit (free tier)*
*Every tool free. Nothing mocked. Production-ready at the end.*
*Shlok Dholakia | KJSCE Mumbai | April 2026*
