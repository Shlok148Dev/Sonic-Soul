"""
PSYCHE API — FastAPI backend serving all 12 agents.

Endpoints:
- POST /recommend — get recommendations
- POST /cold-start/message — cold start interview (SSE streaming)
- GET /health — system health
- WS /ws/agents — real-time agent status
- WS /ws/listener-state — real-time listener state updates
"""

import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

app = FastAPI(
    title="PSYCHE API",
    description="Multi-agent music intelligence API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://psyche.fm"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request/Response Models ---


class RecommendRequest(BaseModel):
    """Recommendation request."""
    user_id: str = Field(..., description="User identifier")
    n: int = Field(default=10, ge=1, le=50, description="Number of recommendations")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Session context")


class RecommendResponse(BaseModel):
    """Recommendation response."""
    recommendations: List[Dict[str, Any]]
    agent_weights: Dict[str, float]
    total_latency_ms: float
    listener_state: Dict[str, Any]


class ColdStartMessageRequest(BaseModel):
    """Cold start interview message."""
    user_id: str
    turn: int = Field(..., ge=1, le=5)
    user_answer: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    agents: Dict[str, Any]
    uptime_seconds: float


# --- Startup ---

_start_time = time.time()


@app.on_event("startup")
async def startup():
    """Initialize orchestrator and agents on startup."""
    logger.info("PSYCHE API starting up...")
    from psyche.registry import build_orchestrator
    try:
        app.state.orchestrator = build_orchestrator()
        logger.info("Orchestrator successfully initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        app.state.orchestrator = None


# --- Endpoints ---


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """System health check — returns all agent statuses."""
    agents_status = {}
    if getattr(app.state, "orchestrator", None):
        agents_status = app.state.orchestrator.health()
    return HealthResponse(
        status="healthy" if agents_status else "degraded",
        agents=agents_status,
        uptime_seconds=time.time() - _start_time,
    )


@app.post("/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    """Get music recommendations for a user."""
    # TODO: Wire to PsycheMetaOrchestrator.recommend()
    return RecommendResponse(
        recommendations=[],
        agent_weights={},
        total_latency_ms=0.0,
        listener_state={"status": "not_initialized"},
    )


@app.post("/cold-start/message")
async def cold_start_message(request: ColdStartMessageRequest):
    """Process a cold start interview message."""
    if not getattr(app.state, "orchestrator", None) or "cold_start" not in app.state.orchestrator._agents:
        return {
            "next_question": None,
            "radar_delta": {},
            "agent_response": "Cold start agent not available.",
            "interview_complete": False,
        }
    
    agent = app.state.orchestrator._agents["cold_start"]
    try:
        response = await agent.infer(
            turn=request.turn, user_answer=request.user_answer, user_id=request.user_id
        )
        return response
    except Exception as e:
        logger.error(f"Cold Start inference failed: {e}")
        return agent.fallback(turn=request.turn)


@app.get("/explain/{track_id}")
async def explain_recommendation(track_id: str, user_id: str = "anonymous"):
    """Get explanation for why a track was recommended."""
    # TODO: Wire to SonicExplainabilityAgent
    return {
        "track_id": track_id,
        "explanation": "Explanation agent not yet initialized.",
    }


@app.get("/integrity/check/{track_id}")
async def check_integrity(track_id: str):
    """Check content integrity for a track (AI Content Shield)."""
    # TODO: Wire to ContentIntegrityGuardian
    return {
        "track_id": track_id,
        "ai_generated": 0.0,
        "toxic": 0.0,
        "spoofed": 0.0,
        "passed": True,
    }


# --- WebSocket Endpoints ---


@app.websocket("/ws/listener-state")
async def ws_listener_state(websocket: WebSocket):
    """Stream listener state updates every 90 seconds."""
    await websocket.accept()
    try:
        while True:
            state = {
                "valence": 0.0,
                "arousal": 0.0,
                "focus": 0.5,
                "social_mode": 0.2,
                "confidence": 0.0,
                "method": "not_initialized",
            }
            if getattr(app.state, "orchestrator", None) and "esie" in app.state.orchestrator._agents:
                agent = app.state.orchestrator._agents["esie"]
                try:
                    # In a real app, signals would be retrieved from db/cache for the user
                    result = await agent.infer()
                    state = result.model_dump()
                except Exception as e:
                    logger.error(f"ESIE inference failed: {e}")
                    result = agent.fallback()
                    state = result.model_dump()
            
            await websocket.send_json(state)
            await asyncio.sleep(90)
    except WebSocketDisconnect:
        logger.info("Listener state WebSocket disconnected")


@app.websocket("/ws/agents")
async def ws_agents(websocket: WebSocket):
    """Stream agent status updates."""
    await websocket.accept()
    try:
        while True:
            # TODO: Wire to orchestrator.health()
            await websocket.send_json({"agents": [], "status": "not_initialized"})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        logger.info("Agent status WebSocket disconnected")
