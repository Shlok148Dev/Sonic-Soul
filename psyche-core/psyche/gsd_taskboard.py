"""
GSD (Grok Session Director) Task Board.

This file defines the GSD sprint plan for PSYCHE development.
GSD reads this to understand what to work on and in what order.
"""

SPRINT_PLAN = {
    "project": "PSYCHE",
    "methodology": "kanban_with_weekly_sprints",
    "current_sprint": "Sprint 1 — Foundation & Data Pipeline",
    "sprints": [
        {
            "name": "Sprint 1 — Foundation & Data Pipeline",
            "week": 1,
            "status": "in_progress",
            "tasks": [
                {"id": "S1-01", "title": "Monorepo scaffolding", "status": "done"},
                {"id": "S1-02", "title": "BasePsycheAgent protocol", "status": "done"},
                {"id": "S1-03", "title": "Pydantic data models", "status": "done"},
                {"id": "S1-04", "title": "Config system", "status": "done"},
                {"id": "S1-05", "title": "CI/CD pipeline", "status": "done"},
                {"id": "S1-06", "title": "FMA dataset download", "status": "in_progress"},
                {"id": "S1-07", "title": "FMA validation pipeline", "status": "todo"},
                {"id": "S1-08", "title": "Librosa feature extraction", "status": "todo"},
                {"id": "S1-09", "title": "FAISS index build", "status": "todo"},
                {"id": "S1-10", "title": "Baselines B0-B4", "status": "in_progress"},
                {"id": "S1-11", "title": "EXP-01: MERT vs MFCC", "status": "todo"},
            ],
        },
        {
            "name": "Sprint 2 — ESIE & Cold Start",
            "week": 2,
            "status": "upcoming",
            "tasks": [
                {"id": "S2-01", "title": "ESIE Ollama integration", "status": "todo"},
                {"id": "S2-02", "title": "ESIE signal heuristic tuning", "status": "todo"},
                {"id": "S2-03", "title": "Cold Start interview flow", "status": "todo"},
                {"id": "S2-04", "title": "Cold Start SSE streaming", "status": "todo"},
                {"id": "S2-05", "title": "Sonic Genome builder", "status": "todo"},
                {"id": "S2-06", "title": "EXP-02: Cold Start quality", "status": "todo"},
            ],
        },
        {
            "name": "Sprint 3 — Micro-Event & Serendipity",
            "week": 3,
            "status": "upcoming",
            "tasks": [
                {"id": "S3-01", "title": "Demucs stem separation", "status": "todo"},
                {"id": "S3-02", "title": "Micro-Event attribution engine", "status": "todo"},
                {"id": "S3-03", "title": "Serendipity CLAP search", "status": "todo"},
                {"id": "S3-04", "title": "Novelty sweet spot tuning", "status": "todo"},
                {"id": "S3-05", "title": "EXP-03: Serendipity rate", "status": "todo"},
            ],
        },
        {
            "name": "Sprint 4 — Fairness RL",
            "week": 4,
            "status": "upcoming",
            "tasks": [
                {"id": "S4-01", "title": "Gymnasium environment", "status": "done"},
                {"id": "S4-02", "title": "PPO training pipeline", "status": "todo"},
                {"id": "S4-03", "title": "Artist diversity reward tuning", "status": "todo"},
                {"id": "S4-04", "title": "Fairness Observatory data", "status": "todo"},
                {"id": "S4-05", "title": "EXP-04: Gini improvement", "status": "todo"},
            ],
        },
    ],
}
