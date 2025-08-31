"""
Frontend Worker Runner
=====================
Execution script for frontend worker with protocol compliance.
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

from .models import FrontendOutput
from .agent import frontend_agent
from ..shared.tools import iso_now


def log_event(session_id: str, event_type: str, agent: str, details: Any):
    """Log event using protocol infrastructure"""
    try:
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": agent})
        logger = LoggingProtocol(cfg)
        logger.log_event(event_type, details)
    except Exception as e:
        print(f"Logging failed: {e}")


def log_debug(session_id: str, message: str, details: Any):
    """Log debug message using protocol infrastructure"""
    try:
        cfg = ProtocolConfig(
            {"session_id": session_id, "agent_name": "frontend-worker"}
        )
        logger = LoggingProtocol(cfg)
        logger.log_debug(message, details)
    except Exception as e:
        print(f"Debug logging failed: {e}")


def update_session_state(session_id: str, state_update: Dict[str, Any]):
    """Update session state using protocol infrastructure"""
    try:
        SessionManagement.update_session_state(session_id, state_update)
        log_debug(
            session_id, "Session state updated", {"keys": list(state_update.keys())}
        )
    except Exception as e:
        log_debug(session_id, "Session state update failed", {"error": str(e)})


def run_frontend_implementation(
    session_id: str, task_description: str, model: str
) -> FrontendOutput:
    """Run frontend worker with AI implementation"""
    worker = "frontend-worker"
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
                "component_architecture",
                "state_management",
                "ui_optimization",
                "responsive_design",
                "accessibility_implementation",
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
            session_id, "Starting frontend implementation", {"task": task_description}
        )
        
        # Log analysis started event for behavior tracking
        log_event(
            session_id,
            "analysis_started",
            worker,
            {
                "task": task_description,
                "analysis_type": "frontend_implementation",
                "timestamp": timestamp,
            },
        )

        # Execute frontend agent
        result = frontend_agent.run_sync(
            f"""Implement frontend components, UI optimizations, and state management.

Task: {task_description}
Session: {session_id}

Perform comprehensive frontend implementation including:
1. Component architecture design and implementation
2. State management integration and optimization
3. UI/UX optimizations and performance improvements
4. Responsive design and accessibility compliance
5. Styling and design system integration
6. Frontend testing and quality assurance

Focus on user experience, performance, and maintainable code architecture.""",
            model=model,
        )

        output: FrontendOutput = result.output

        # Framework-enforced output validation ensures structure
        if not output.worker:
            output.worker = worker
        if not output.session_id:
            output.session_id = session_id
        if not output.timestamp:
            output.timestamp = timestamp

        log_debug(
            session_id,
            "Frontend implementation completed",
            {
                "component_implementations": len(output.component_implementations),
                "state_management_changes": len(output.state_management_changes),
                "ui_optimizations": len(output.ui_optimizations),
                "component_architecture_score": output.component_architecture_score,
                "state_architecture_score": output.state_architecture_score,
                "ui_performance_score": output.ui_performance_score,
            },
        )

        # Create implementation files using protocol infrastructure
        create_frontend_files(session_id, output)

        # Update session state to completed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "completed",
                f"{worker}_completed": timestamp,
                f"{worker}_component_architecture": output.component_architecture_score,
                f"{worker}_state_architecture": output.state_architecture_score,
                f"{worker}_ui_performance": output.ui_performance_score,
                f"{worker}_frontend_quality": output.frontend_quality_score,
            },
        )

        # Log completion
        log_event(
            session_id,
            "worker_completed",
            worker,
            {
                "duration": "calculated",
                "components_count": len(output.component_implementations),
                "state_changes_count": len(output.state_management_changes),
                "optimizations_count": len(output.ui_optimizations),
                "status": output.status,
            },
        )

        return output

    except Exception as e:
        log_debug(
            session_id,
            "Frontend implementation failed",
            {"error": str(e), "task": task_description},
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

        )

        raise


def create_frontend_files(session_id: str, output: FrontendOutput):
    """Create frontend output files using protocol infrastructure"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        notes_dir = session_path / "workers" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Create frontend notes file if content provided
        if output.notes_markdown:
            notes_file = notes_dir / "frontend_notes.md"
            notes_file.write_text(output.notes_markdown)
            log_debug(
                session_id, "Created frontend notes file", {"path": str(notes_file)}
            )

        # Create structured output JSON
        output_file = notes_dir / "frontend_output.json"
        output_file.write_text(output.model_dump_json(indent=2))
        log_debug(
            session_id, "Created frontend output JSON", {"path": str(output_file)}
        )

    except Exception as e:
        log_debug(session_id, "File creation failed", {"error": str(e)})


def main():
    """CLI entry point for frontend worker"""
    parser = argparse.ArgumentParser(
        description="Frontend Worker - UI/UX Implementation"
    )
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument(
        "--task", required=True, help="Frontend implementation task description"
    )
    parser.add_argument("--model", default="openai:gpt-5", help="AI model to use")

    args = parser.parse_args()

    try:
        output = run_frontend_implementation(args.session, args.task, args.model)
        print(
            f"Frontend implementation completed. Quality score: {output.frontend_quality_score}, UX score: {output.user_experience_score}, Accessibility: {output.accessibility_score}"
        )
        return 0
    except Exception as e:
        print(f"Frontend worker failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
