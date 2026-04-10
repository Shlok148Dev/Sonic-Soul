"""
PSYCHE API — FastAPI backend serving all 12 agents.

Endpoints:
- POST /recommend — get recommendations
- POST /cold-start/message — cold start interview (SSE streaming)
- GET /explain/{track_id} — get explanations
- GET /integrity/check/{track_id} — content verification
- GET /health — system health
- WS /ws/agents — real-time agent status
- WS /ws/listener-state — real-time listener state updates
"""

import asyncio
import json
import logging
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from psyche.models.listener_state import ListenerStateVector
from psyche.db.supabase_client import PsycheDBClient
from psyche.db.cache import PsycheCache

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
    user_id: str = Field(..., description="User identifier")
    n: int = Field(default=10, ge=1, le=50, description="Number of recommendations")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Session context")

class RecommendResponse(BaseModel):
    recommendations: List[Any]
    agent_weights: Dict[str, float]
    total_latency_ms: float
    listener_state: Dict[str, Any]

class ColdStartMessageRequest(BaseModel):
    user_id: str
    turn: int = Field(..., ge=1, le=5)
    user_answer: str

class HealthResponse(BaseModel):
    status: str
    agents: Dict[str, Any]
    uptime_seconds: float


# --- Startup ---

_start_time = time.time()

@app.on_event("startup")
async def startup():
    """Initialize orchestrator, cache, and db on startup."""
    logger.info("PSYCHE API starting up...")
    from psyche.registry import build_orchestrator
    try:
        app.state.orchestrator = build_orchestrator()
        app.state.db = PsycheDBClient.get_instance()
        app.state.cache = PsycheCache()
        logger.info("Orchestrator successfully initialized.")
    except Exception as e:
        logger.error(f"Failed to initialize orchestrator: {e}")
        app.state.orchestrator = None


# --- Middleware ---
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """
    Apply Upstash Redis Rate Limiting across all routes.
    Simulated 50 requests / minute / IP
    """
    if getattr(app.state, "cache", None) and request.client:
        ip = request.client.host
        key = f"rate_limit:{ip}"
        
        # Pull hits
        client_hits = app.state.cache.get(key) or 0
        if client_hits > 50:
            from fastapi.responses import JSONResponse
            return JSONResponse({"error": "Rate limit exceeded (50/min)"}, status_code=429)
        
        app.state.cache.set(key, client_hits + 1, ttl_seconds=60)
        
    response = await call_next(request)
    return response


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
    if not getattr(app.state, "orchestrator", None):
        raise HTTPException(status_code=500, detail="Orchestrator unavailable")
        
    # Attempt to pull ESIE state from cache
    cache = app.state.cache
    db = app.state.db
    
    state_dict = cache.get_listener_state(request.user_id) if cache else None
    
    if not state_dict:
        # Fallback to defaults
        state = ListenerStateVector(valence=0.5, arousal=0.5, focus=0.5, social_mode=0.5, confidence=0.0, method="fallback")
    else:
        state = ListenerStateVector(**state_dict)
        
    try:
        response = await app.state.orchestrator.recommend(
            listener_state=state,
            n=request.n,
            context=request.context
        )
        return response
    except Exception as e:
        logger.error(f"Recommendation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


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
    if not getattr(app.state, "orchestrator", None) or "explainability" not in app.state.orchestrator._agents:
        return {"explanation": "Explanation offline."}

    cache = getattr(app.state, "cache", None)
    if cache:
        cached = cache.get_explanation(track_id, user_id)
        if cached:
            return {"track_id": track_id, "explanation": cached}

    agent = app.state.orchestrator._agents["explainability"]
    try:
        res = await agent.infer(track_name=track_id, artist="Unknown", listener_state={"arousal": 0.8})
        if cache:
            cache.cache_explanation(track_id, user_id, res["explanation"])
        return {"track_id": track_id, "explanation": res["explanation"]}
    except Exception as e:
        return {"track_id": track_id, "explanation": agent.fallback(track_name=track_id)["explanation"]}


@app.get("/integrity/check/{track_id}")
async def check_integrity(track_id: str):
    """Check content integrity for a track (AI Content Shield)."""
    if getattr(app.state, "orchestrator", None) and "content_integrity" in app.state.orchestrator._agents:
        agent = app.state.orchestrator._agents["content_integrity"]
        score = await agent.infer(track_id=track_id, metadata={"title": "test", "artist": "test"})
        return score.model_dump()
        
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
            status_map = {"status": "degraded"}
            if getattr(app.state, "orchestrator", None):
                status_map = app.state.orchestrator.health()
            await websocket.send_json(status_map)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        logger.info("Agent status WebSocket disconnected")
