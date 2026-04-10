# PSYCHE — MODEL HANDOFF FILE
# ============================
# READ THIS FIRST. This is the single source of truth for AI model continuity.
# When switching models, the new model MUST read this file before doing anything else.

## Current State
- **Date**: 2026-04-10
- **Phase**: Week 1, Day 1 — Repository Foundation COMPLETE
- **Last Completed**: Full monorepo scaffolded, committed, pushed to GitHub
- **Currently Working On**: Next → Week 1, Days 3-5 (Data Pipeline)
- **Branch**: `main`
- **Git Commit**: b8caff3

## What Has Been Done
1. ✅ Read both PSYCHE_ULTIMATE_MASTERPLAN.md and PSYCHE_DEVELOPMENT_GUIDE.md fully
2. ✅ Created monorepo structure for all 5 components:
   - psyche-core/ — Python SDK + 12 implemented agents + orchestrator
   - psyche-api/ — FastAPI backend with all endpoints
   - psyche-bench/ — Benchmark CLI skeleton
   - psyche-plugins/ — VS Code extension structure + Discord bot
3. ✅ Created .gitignore, LICENSE, README.md, SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md
4. ✅ Created agent knowledge base (.agents/skills/ + rules.md)
5. ✅ Created BasePsycheAgent protocol (psyche/agents/base.py)
6. ✅ Created all 12 agent implementations:
   - ESIE (esie.py) — Emotional State Inference Engine
   - Cold Start (cold_start.py) — Psychographic Interview
   - Fairness RL (fairness_rl.py) — PPO-based with artist diversity
   - SEA (sea.py) — Sonic Explainability Agent
   - Serendipity (serendipity.py) — CLAP novelty search
   - Coherence (coherence.py) — Playlist energy arc
   - Integrity (integrity.py) — Content Integrity Guardian
   - Micro-Event (micro_event.py) — Stem attribution
   - Temporal Taste (temporal_taste.py) — GRU taste evolution
   - Context Fusion (context_fusion.py) — Environmental context
   - Intent Classifier (intent_classifier.py) — Active/passive/background
   - Rumination Guard (rumination_guard.py) — Mental health protection
7. ✅ Created all Pydantic data models (ListenerStateVector, Track, SonicGenome, etc.)
8. ✅ Created PsycheMetaOrchestrator
9. ✅ Created data pipelines (FMA ingestion, feature extraction, FAISS index)
10. ✅ Created config system (configs/config.yaml + PsycheConfig)
11. ✅ Created Docker environment (Dockerfile + docker-compose.yml)
12. ✅ Created CI/CD workflows (ci.yml + release.yml)
13. ✅ Created CodeRabbit config (.coderabbit.yaml)
14. ✅ Created pyproject.toml and requirements files
15. ✅ Created evaluation metrics (serendipity, gini, coherence, P@K, R@K)
16. ✅ Created unit tests (BasePsycheAgent, ESIE, models)
17. ✅ Created FMA download script
18. ✅ Pushed to GitHub: https://github.com/Shlok148Dev/Sonic-Soul

## What Needs To Be Done Next
1. **Week 1, Days 3-5: Data Pipeline** (IMMEDIATE PRIORITY)
   - Download FMA-small dataset (~7.2GB)
   - Run ingestion/validation pipeline
   - Feature extraction (librosa MFCCs, spectral features)
   - MERT embedding generation (768-dim)
   - CLAP embedding generation (512-dim)
   - FAISS index build for both MERT and CLAP
2. **Week 1, Days 6-7: Baselines B0-B4**
   - B0: Random recommender
   - B1: Popularity-weighted random
   - B2: MFCC cosine similarity
   - B3: CLAP cosine similarity
   - B4: ALS collaborative filtering
   - EXP-01: MERT vs MFCC retrieval quality
3. **Week 2: ESIE + Cold Start** (full inference wiring)
4. Continue per PSYCHE_DEVELOPMENT_GUIDE.md

## Key Files to Read
- `PSYCHE_ULTIMATE_MASTERPLAN.md` — THE masterplan
- `PSYCHE_DEVELOPMENT_GUIDE.md` — THE step-by-step build guide
- `HANDOFF.md` — THIS FILE
- `psyche-core/psyche/agents/base.py` — BasePsycheAgent protocol
- `psyche-core/psyche/orchestrator.py` — Meta-orchestrator
- `configs/config.yaml` — all system configuration
- `.agents/rules.md` — global agent rules

## Environment State
- **OS**: Windows 11
- **Python**: 3.10.8
- **Node.js**: v22.19.0
- **Docker**: 29.3.0
- **Git**: 2.52.0
- **Workspace**: c:\Users\hp\Desktop\Sonic Soul
- **GitHub Repo**: https://github.com/Shlok148Dev/Sonic-Soul.git
- **Branch**: main

## Accounts Status (User Needs To Create)
- [ ] Weights & Biases (wandb.ai) — needed for experiment logging
- [ ] Hugging Face (huggingface.co) — needed for MERT/CLAP model access
- [ ] Vercel (vercel.com) — needed for psyche-ui deployment
- [ ] Supabase (supabase.com) — needed for user data store
- [ ] Upstash (upstash.com) — needed for explanation cache
- [ ] CodeRabbit (app.coderabbit.ai) — install on GitHub repo
- [ ] Railway (railway.app) — needed for API deployment
- [ ] Anthropic (console.anthropic.com) — free tier credits

## Instructions For New Model
1. Read this file FIRST
2. Read PSYCHE_ULTIMATE_MASTERPLAN.md for full context
3. Read PSYCHE_DEVELOPMENT_GUIDE.md for exact build steps
4. Check git log to see what's been committed
5. Check the "What Needs To Be Done Next" section above
6. Continue from exactly where the previous model left off
7. Update this HANDOFF.md file when you complete tasks or hit blockers
8. NEVER re-do work that's already completed — check git history

## Blockers Requiring User Action
- Account creation for free-tier services listed above
- Ollama installation for local LLM inference (install from ollama.com)
- ~7.2GB disk space for FMA-small dataset download
