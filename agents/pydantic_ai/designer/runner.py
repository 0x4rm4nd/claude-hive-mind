"""
Designer Worker Runner
=====================
Execution script for designer worker with protocol compliance.
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

from .models import DesignerOutput
from .agent import designer_agent
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
            {"session_id": session_id, "agent_name": "designer-worker"}
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


def run_designer_analysis(
    session_id: str, task_description: str, model: str
) -> DesignerOutput:
    """Run designer worker with AI analysis"""
    worker = "designer-worker"
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
                "user_experience_design",
                "visual_design",
                "accessibility_compliance",
                "design_systems",
                "responsive_design",
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
        # Log analysis started event for behavior tracking
        log_event(
            session_id,
            "analysis_started",
            worker,
            {
                "task": task_description,
                "analysis_type": "design_analysis",
                "timestamp": timestamp,
            },
        )

        # Execute designer agent
        result = designer_agent.run_sync(
            f"""Analyze the user interface design and provide UX/UI recommendations.

Task: {task_description}
Session: {session_id}

Perform comprehensive design analysis including:
1. User experience evaluation and journey mapping
2. Visual design assessment and brand consistency review
3. Accessibility compliance audit (WCAG guidelines)
4. Design system evaluation and component analysis
5. Responsive design and cross-platform consistency
6. Information architecture and navigation optimization

Focus on user-centered improvements that enhance usability and accessibility.""",
            model=model,
        )

        output: DesignerOutput = result.output

        # Framework-enforced output validation ensures structure
        if not output.worker:
            output.worker = worker
        if not output.session_id:
            output.session_id = session_id
        if not output.timestamp:
            output.timestamp = timestamp

        # Create analysis file using protocol infrastructure
        create_designer_files(session_id, output)

        # Update session state to completed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "completed",
                f"{worker}_completed": timestamp,
                f"{worker}_design_maturity": output.design_maturity_score,
                f"{worker}_accessibility": output.accessibility_score,
                f"{worker}_usability": output.usability_score,
                f"{worker}_design_quality": output.design_quality_score,
            },
        )

        # Log completion
        log_event(
            session_id,
            "worker_completed",
            worker,
            {
                "duration": "calculated",
                "recommendations_count": len(output.design_recommendations),
                "accessibility_findings_count": len(output.accessibility_findings),
                "status": output.status,
            },
        )

        return output

    except Exception as e:
        log_debug(
            session_id,
            "Designer analysis failed",
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

        raise


def create_designer_files(session_id: str, output: DesignerOutput):
    """Create designer output files using protocol infrastructure"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        notes_dir = session_path / "workers" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Create designer notes file if content provided
        if output.notes_markdown:
            notes_file = notes_dir / "designer_notes.md"
            notes_file.write_text(output.notes_markdown)
            log_debug(
                session_id, "Created designer notes file", {"path": str(notes_file)}
            )

        # Create structured output JSON
        output_file = notes_dir / "designer_output.json"
        output_file.write_text(output.model_dump_json(indent=2))
        log_debug(
            session_id, "Created designer output JSON", {"path": str(output_file)}
        )

    except Exception as e:
        log_debug(session_id, "File creation failed", {"error": str(e)})


def main():
    """CLI entry point for designer worker"""
    parser = argparse.ArgumentParser(
        description="Designer Worker - UX/UI Design Analysis"
    )
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--task", required=True, help="Design task description")
    parser.add_argument("--model", default="openai:gpt-5", help="AI model to use")

    args = parser.parse_args()

    try:
        output = run_designer_analysis(args.session, args.task, args.model)
        print(
            f"Design analysis completed. Quality score: {output.design_quality_score}, Accessibility: {output.accessibility_score}, Usability: {output.usability_score}"
        )
        return 0
    except Exception as e:
        print(f"Designer worker failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
