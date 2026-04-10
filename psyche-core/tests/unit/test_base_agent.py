"""Unit tests for BasePsycheAgent protocol."""

import asyncio
import pytest

from psyche.agents.base import BasePsycheAgent, AgentHealthStatus


class MockAgent(BasePsycheAgent):
    """Test agent that implements the protocol."""

    @property
    def name(self) -> str:
        return "mock_agent"

    async def infer(self, **kwargs):
        if kwargs.get("fail", False):
            raise RuntimeError("Intentional test failure")
        return {"result": "success", "input": kwargs}

    def fallback(self, **kwargs):
        return {"result": "fallback", "input": kwargs}


class TestBasePsycheAgent:
    """Test the BasePsycheAgent contract."""

    def test_agent_name(self):
        agent = MockAgent()
        assert agent.name == "mock_agent"

    @pytest.mark.asyncio
    async def test_run_success(self):
        agent = MockAgent()
        result = await agent.run(test_input="hello")
        assert result["agent"] == "mock_agent"
        assert result["used_fallback"] is False
        assert result["latency_ms"] > 0
        assert result["result"]["result"] == "success"

    @pytest.mark.asyncio
    async def test_run_fallback(self):
        agent = MockAgent()
        result = await agent.run(fail=True)
        assert result["agent"] == "mock_agent"
        assert result["used_fallback"] is True
        assert result["result"]["result"] == "fallback"

    def test_health_check(self):
        agent = MockAgent()
        health = agent.health_check()
        assert isinstance(health, AgentHealthStatus)
        assert health.agent_name == "mock_agent"
        assert health.status == "healthy"
