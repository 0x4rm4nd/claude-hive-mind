"""
Claude API Service Server

Simple HTTP API service that routes Pydantic AI requests through Claude CLI.
Eliminates nested subprocess authentication issues for Max subscription integration.
"""

import asyncio
import logging
import os
import json
from typing import Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

from claude_client import ClaudeClient

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Claude API Service",
    description="Simple Claude CLI service for Pydantic AI Max subscription integration",
    version="1.0.0",
)

# Initialize Claude client
claude_client = ClaudeClient()


# Request/Response models
class ClaudeRequest(BaseModel):
    prompt: str
    model: str = "sonnet"
    timeout: int = 120


# Core API Endpoints


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    claude_healthy = await claude_client.health_check()

    return {
        "status": "healthy" if claude_healthy else "degraded",
        "claude_cli": "available" if claude_healthy else "unavailable",
        "workspace_root": str(claude_client.workspace_root),
        "purpose": "Max subscription integration via Docker",
    }


@app.post("/claude")
async def claude_request(request: ClaudeRequest):
    """Generic Claude CLI proxy for any Pydantic AI request"""
    logger.info(
        f"Claude request: {request.model}, prompt length: {len(request.prompt)}"
    )

    try:
        response = await claude_client.run_claude_command(
            prompt=request.prompt, model=request.model, timeout=request.timeout
        )

        return {"response": response, "model": request.model, "success": True}

    except Exception as e:
        logger.error(f"Claude request failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Root endpoint with service info"""
    return {
        "service": "Claude API Service",
        "purpose": "Max subscription integration for Pydantic AI",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Service health check",
            "/claude": "Generic Claude CLI proxy for any Pydantic AI request",
        },
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Claude API Service on port {port}")

    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info", access_log=True)
