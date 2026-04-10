"""Tests for the Content Integrity Guardian."""

import pytest
from psyche.config import PsycheConfig
from psyche.agents.integrity import ContentIntegrityGuardian

class TestContentIntegrityGuardian:
    def test_safe_metadata_passes(self):
        config = PsycheConfig()
        agent = ContentIntegrityGuardian(config)
        
        # Testing basic logic (we mock the async infer by testing the code directly or handling awaited mock)
        import asyncio
        score = asyncio.run(agent.infer(track_id="safe-123", metadata={"title": "Ocean Waves", "artist": "Nature Sounds"}))
        assert score.passed is True
        assert score.toxic == 0.0
        assert score.ai_generated == 0.0

    def test_toxic_metadata_fails(self):
        config = PsycheConfig()
        agent = ContentIntegrityGuardian(config)
        
        import asyncio
        score = asyncio.run(agent.infer(track_id="toxic-123", metadata={"title": "Hate world", "artist": "Angry Guy"}))
        assert score.passed is False
        assert score.toxic == 1.0

    def test_ai_metadata_fails(self):
        config = PsycheConfig()
        agent = ContentIntegrityGuardian(config)
        
        import asyncio
        score = asyncio.run(agent.infer(track_id="ai-123", metadata={"title": "AI Cover of song", "artist": "Suno"}))
        assert score.passed is False
        assert score.ai_generated == 1.0
