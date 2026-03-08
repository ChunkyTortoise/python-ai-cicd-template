"""FastAPI application entry point."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.config import settings

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Python AI service",
)

# Job storage (in-memory for demo)
_jobs: dict[str, dict[str, Any]] = {}


class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: int = 100


class GenerateResponse(BaseModel):
    job_id: str
    status: str
    result: str | None = None


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    """Generate text via LLM (mock). Replace with real Claude API call."""
    job_id = str(uuid.uuid4())[:8]

    # Mock response -- replace with: anthropic.Anthropic().messages.create(...)
    mock_result = f"Mock response to: {request.prompt[:50]}"

    _jobs[job_id] = {
        "id": job_id,
        "status": "complete",
        "result": mock_result,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "prompt": request.prompt,
    }

    return GenerateResponse(job_id=job_id, status="complete", result=mock_result)


@app.get("/api/status/{job_id}", response_model=GenerateResponse)
async def get_job_status(job_id: str) -> GenerateResponse:
    """Get status of a generate job."""
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    job = _jobs[job_id]
    return GenerateResponse(
        job_id=job["id"],
        status=job["status"],
        result=job.get("result"),
    )
