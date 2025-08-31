"""
Backend Worker Runner
====================
Execution script for backend worker with protocol compliance.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import sys
import os

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from ..shared.protocols import (
    SessionManagement,
    LoggingProtocol,
    ProtocolConfig,
    WorkerPromptProtocol,
)

from .models import BackendOutput
from .agent import backend_agent
from ..shared.tools import iso_now


def log_event(session_id: str, event_type: str, agent: str, details: Any):
    """Log event using protocol infrastructure"""
    try:
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": agent})
        logger = LoggingProtocol(cfg)
        logger.log_event(event_type, details)
    except Exception as e:
        print(f"Logging failed: {e}")


def log_debug(session_id: str, message: str, details: Any, level: str = "DEBUG"):
    """Log debug message using protocol infrastructure"""
    try:
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": "backend-worker"})
        logger = LoggingProtocol(cfg)
        logger.log_debug(message, details, level)
    except Exception as e:
        print(f"Debug logging failed: {e}")


def update_session_state(session_id: str, state_update: Dict[str, Any]):
    """Update session state using protocol infrastructure"""
    try:
        SessionManagement.update_state_atomically(session_id, state_update)
        log_debug(
            session_id, "Session state updated", {"keys": list(state_update.keys())}
        )
    except Exception as e:
        log_debug(session_id, "Session state update failed", {"error": str(e)}, "ERROR")


def run_backend_implementation(
    session_id: str, task_description: str, model: str
) -> BackendOutput:
    """Run backend worker with AI implementation"""
    worker = "backend-worker"
    timestamp = iso_now()

    # Validate session exists using protocol infrastructure
    try:
        if not SessionManagement.ensure_session_exists(session_id):
            raise ValueError(f"Session {session_id} does not exist or is invalid")
        log_debug(
            session_id, "Session validation successful", {"session_id": session_id}
        )
    except Exception as e:
        log_debug(
            session_id,
            "Session validation failed",
            {"error": str(e), "session_id": session_id},
        )

    # Log worker spawn
    log_event(
        session_id,
        "worker_spawned",
        worker,
        {
            "task": task_description,
            "model": model,
            "timestamp": timestamp,
            "capabilities": [
                "architecture_analysis",
                "api_development",
                "database_optimization",
                "system_optimization", 
                "scalability_assessment",
            ],
        },
    )

    # Update session state
    update_session_state(
        session_id,
        {
            f"{worker}_status": "running",
            f"{worker}_started": timestamp,
            f"{worker}_task": task_description,
        },
    )

    try:
        log_debug(
            session_id, "Starting backend implementation", {"task": task_description}
        )
        
        # Log analysis started event for behavior tracking
        log_event(
            session_id,
            "analysis_started",
            worker,
            {
                "task": task_description,
                "analysis_type": "backend_implementation",
                "timestamp": timestamp,
            },
        )

        # Execute backend agent
        result = backend_agent.run_sync(
            f"""Analyze and optimize backend systems, APIs, and architecture.

Task: {task_description}
Session: {session_id}

Perform comprehensive backend analysis and optimization including:
1. Architecture assessment and improvement recommendations  
2. API design patterns and performance optimization
3. Database schema optimization and query performance tuning
4. System scalability and performance bottleneck analysis
5. Integration patterns and service boundary optimization
6. Security, caching, and resilience pattern recommendations

Provide specific, actionable improvements with detailed technical rationale and implementation guidance.""",
            model=model,
        )

        output: BackendOutput = result.output

        # Framework-enforced output validation ensures structure
        if not output.worker:
            output.worker = worker
        if not output.session_id:
            output.session_id = session_id
        if not output.timestamp:
            output.timestamp = timestamp

        log_debug(
            session_id,
            "Backend implementation completed",
            {
                "api_endpoints": len(output.api_endpoints),
                "database_changes": len(output.database_changes),
                "service_implementations": len(output.service_implementations),
                "api_design_score": output.api_design_score,
                "database_design_score": output.database_design_score,
                "service_architecture_score": output.service_architecture_score,
                "backend_quality_score": output.backend_quality_score,
            },
        )

        # Create implementation files using protocol infrastructure
        create_backend_files(session_id, output)

        # Update session state to completed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "completed",
                f"{worker}_completed": timestamp,
                f"{worker}_api_design": output.api_design_score,
                f"{worker}_database_design": output.database_design_score,
                f"{worker}_service_architecture": output.service_architecture_score,
                f"{worker}_backend_quality": output.backend_quality_score,
            },
        )

        # Log completion
        log_event(
            session_id,
            "worker_completed",
            worker,
            {
                "duration": "calculated",
                "api_endpoints_count": len(output.api_endpoints),
                "database_changes_count": len(output.database_changes),
                "service_implementations_count": len(output.service_implementations),
                "status": output.status,
            },
        )

        return output

    except Exception as e:
        log_debug(
            session_id,
            "Backend implementation failed",
            {"error": str(e), "task": task_description},
            "ERROR"
        )

        # Update session state to failed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "failed",
                f"{worker}_error": str(e),
                f"{worker}_failed": timestamp,
            },
        )


        raise


def create_backend_files(session_id: str, output: BackendOutput):
    """Create backend output files using protocol infrastructure"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        notes_dir = session_path / "workers" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Create backend notes file if content provided
        if output.notes_markdown:
            notes_file = notes_dir / "backend_notes.md"
            notes_file.write_text(output.notes_markdown)
            log_debug(
                session_id, "Created backend notes file", {"path": str(notes_file)}
            )

        # Create structured output JSON
        output_file = notes_dir / "backend_output.json"
        output_file.write_text(output.model_dump_json(indent=2))
        log_debug(session_id, "Created backend output JSON", {"path": str(output_file)})

    except Exception as e:
        log_debug(session_id, "File creation failed", {"error": str(e)}, "ERROR")


def main():
    """CLI entry point for backend worker"""
    parser = argparse.ArgumentParser(
        description="Backend Worker - API and Service Implementation"
    )
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument(
        "--task", required=True, help="Backend implementation task description"
    )
    parser.add_argument("--model", default="openai:gpt-5", help="AI model to use")

    args = parser.parse_args()

    try:
        output = run_backend_implementation(args.session, args.task, args.model)
        print(
            f"Backend implementation completed. Quality score: {output.backend_quality_score}, API design: {output.api_design_score}, Database design: {output.database_design_score}"
        )
        return 0
    except Exception as e:
        print(f"Backend worker failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
