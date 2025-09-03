"""
Claude API Service Server

Simple HTTP API service that routes Pydantic AI requests through Claude CLI.
Eliminates nested subprocess authentication issues for Max subscription integration.
"""

import logging
import os
import json
import time

from fastapi import FastAPI, HTTPException, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from claude_client import ClaudeClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Claude API Service",
    description="Simple Claude CLI service for Pydantic AI Max subscription integration",
    version="1.0.0",
)


# Custom middleware for clean logging (timestamp only, no IP)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    # For /claude endpoint, include response text in logs
    if request.url.path == "/claude" and request.method == "POST":
        # Get response body for logging (only for /claude endpoint)
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        try:
            response_json = json.loads(response_body.decode())
            claude_response = response_json.get("response", "")
            logger.info(
                f'"{request.method} {request.url.path}" {response.status_code} ({process_time:.3f}s) [{claude_response}]'
            )
        except Exception:
            logger.info(
                f'"{request.method} {request.url.path}" {response.status_code} ({process_time:.3f}s)'
            )

        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.headers.get("content-type"),
        )
    else:
        # Clean log format for other endpoints
        logger.info(
            f'"{request.method} {request.url.path}" {response.status_code} ({process_time:.3f}s)'
        )

    return response


# Initialize Claude client
claude_client = ClaudeClient()


# Request/Response models
class ClaudeData(BaseModel):
    prompt: str
    model: str = "sonnet"
    timeout: int = 120


# Core API Endpoints


@app.get("/health", status_code=200)
async def health_check(response: Response):
    """Health check endpoint"""
    claude_healthy = await claude_client.health_check()

    if not claude_healthy:
        response.status_code = 503  # Service Unavailable

    return {
        "status": "healthy" if claude_healthy else "degraded",
        "claude_cli": "available" if claude_healthy else "unavailable",
        "workspace_root": str(claude_client.workspace_root),
        "purpose": "Max subscription integration via Docker",
        "message": (
            "Service ready"
            if claude_healthy
            else "Claude CLI authentication required: docker exec -it claude-max-api claude setup-token"
        ),
    }


@app.post("/claude")
async def claude_request(request: Request, claude_data: ClaudeData):
    """Generic Claude CLI proxy for any Pydantic AI request"""
    logger.info(
        f"Claude request: {claude_data.model}, prompt length: {len(claude_data.prompt)}"
    )

    # Check for system prompt override in headers
    system_prompt_override = request.headers.get("X-System-Prompt-Override", None)

    try:
        response = await claude_client.run_claude_command(
            prompt=claude_data.prompt,
            model=claude_data.model,
            timeout=claude_data.timeout,
            system_prompt_override=system_prompt_override,
        )

        return {"response": response, "model": claude_data.model, "success": True}

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

    # Disable uvicorn's access log since we have custom middleware logging
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=False,  # Disable built-in access logging
    )
