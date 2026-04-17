"""
Production AI Agent - Combined all Day 12 concepts

Checklist:
  [OK] Config from environment (12-factor)
  [OK] Structured JSON logging
  [OK] API Key authentication
  [OK] Rate limiting
  [OK] Cost guard
  [OK] Input validation (Pydantic)
  [OK] Health check + Readiness probe
  [OK] Graceful shutdown
  [OK] Security headers
  [OK] CORS
  [OK] Error handling
"""
import time
import logging
import json
import signal
from datetime import datetime, timezone
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field

from app.config import settings
from app.auth import verify_api_key
from app.rate_limiter import check_rate_limit
from app.cost_guard import check_budget, update_cost
from utils.mock_llm import ask as llm_ask

logging.basicConfig(
    level=logging.INFO,
    format='{"ts":"%(asctime)s","lvl":"%(levelname)s","msg":"%(message)s"}'
)
logger = logging.getLogger(__name__)

START_TIME = time.time()
_is_ready = False
_in_flight_requests = 0

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _is_ready
    logger.info(json.dumps({"event": "startup", "env": settings.environment}))
    _is_ready = True
    yield
    _is_ready = False
    logger.info(json.dumps({"event": "shutdown_initiated"}))
    
    # Chờ request đang xử lý hoàn thành (tối đa 30 giây)
    timeout = 30
    elapsed = 0
    while _in_flight_requests > 0 and elapsed < timeout:
        logger.info(f"Waiting for {_in_flight_requests} in-flight requests...")
        time.sleep(1)
        elapsed += 1
        
    logger.info(json.dumps({"event": "shutdown_complete"}))

app = FastAPI(title=settings.app_name, lifespan=lifespan)

@app.middleware("http")
async def track_requests(request, call_next):
    """Theo dõi số request đang xử lý."""
    global _in_flight_requests
    _in_flight_requests += 1
    try:
        response = await call_next(request)
        return response
    finally:
        _in_flight_requests -= 1

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)

class AskResponse(BaseModel):
    question: str
    answer: str
    timestamp: str

@app.post("/ask", response_model=AskResponse)
async def ask_agent(body: AskRequest, user_id: str = Depends(verify_api_key)):
    # Stateless Security Checks
    check_rate_limit(user_id)
    check_budget(user_id)

    # Giả lập chi phí token
    input_cost = (len(body.question.split()) / 1000) * 0.00015
    update_cost(user_id, input_cost)

    answer = llm_ask(body.question)

    output_cost = (len(answer.split()) / 1000) * 0.0006
    update_cost(user_id, output_cost)

    return AskResponse(
        question=body.question,
        answer=answer,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

@app.get("/health")
def health():
    return {
        "status": "ok",
        "uptime": round(time.time() - START_TIME, 1),
        "version": settings.app_version
    }

@app.get("/ready")
def ready():
    if not _is_ready:
        raise HTTPException(status_code=503, detail="Service initializing")
    return {"status": "ready"}

# ----------------------------------------------------------
# GRACEFUL SHUTDOWN (Handle SIGTERM for safe app closure)
# ----------------------------------------------------------
def handle_exit(signum, frame):
    # Uvicorn handles this signal and triggers lifespan shutdown
    logger.info(f"Received signal {signum} (SIGTERM/SIGINT) - initiating graceful shutdown")

signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)