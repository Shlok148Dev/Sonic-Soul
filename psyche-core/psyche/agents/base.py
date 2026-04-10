"""
BasePsycheAgent — The contract that every PSYCHE agent must implement.

This protocol defines the interface. Every agent is independently testable,
independently fallible, and independently deployable.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import time
import logging
import datetime

logger = logging.getLogger(__name__)


try:
    import wandb
except ImportError:
    wandb = None  # type: ignore[assignment]


from pydantic import BaseModel, ConfigDict, Field


class AgentHealthStatus(BaseModel):
    """Health status of a PSYCHE agent."""

    model_config = ConfigDict(frozen=True)
    agent_name: str = Field(..., description="Agent identifier")
    status: str = Field(..., description="'healthy' | 'degraded' | 'failed'")
    latency_ms: Optional[float] = Field(default=None, description="Last inference latency in ms")
    last_check: str = Field(..., description="ISO timestamp of last health check")
    error: Optional[str] = Field(default=None, description="Error message if status != healthy")


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
    async def infer(self, **kwargs: Any) -> Any:
        """
        Primary inference path. Must be async.
        Raise any exception if inference fails — the base class handles it.
        """
        ...

    @abstractmethod
    def fallback(self, **kwargs: Any) -> Any:
        """
        Fallback path. Called when infer() raises any exception.
        MUST return a valid output of the same type as infer().
        MUST NOT raise exceptions.
        """
        ...

    async def run(self, **kwargs: Any) -> Dict[str, Any]:
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
            if wandb is not None and wandb.run is not None:
                wandb.log(
                    {
                        f"agent/{self.name}/latency_ms": elapsed_ms,
                        f"agent/{self.name}/used_fallback": int(used_fallback),
                    }
                )
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
            last_check=datetime.datetime.utcnow().isoformat(),
        )
