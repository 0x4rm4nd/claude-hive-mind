"""
DevOps Worker Runner
===================
Execution script for DevOps worker with protocol compliance.
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

from .models import DevOpsOutput
from .agent import devops_agent
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
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": "devops-worker"})
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


def run_devops_implementation(
    session_id: str, task_description: str, model: str
) -> DevOpsOutput:
    """Run DevOps worker with AI implementation"""
    worker = "devops-worker"
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
                "infrastructure_management",
                "cicd_pipelines",
                "monitoring_systems",
                "security_automation",
                "deployment_strategies",
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
            session_id, "Starting DevOps implementation", {"task": task_description}
        )
        
        # Log analysis started event for behavior tracking
        log_event(
            session_id,
            "analysis_started",
            worker,
            {
                "task": task_description,
                "analysis_type": "devops_implementation",
                "timestamp": timestamp,
            },
        )

        # Execute DevOps agent
        result = devops_agent.run_sync(
            f"""Implement infrastructure, deployment, and monitoring solutions.

Task: {task_description}
Session: {session_id}

Perform comprehensive DevOps implementation including:
1. Infrastructure design and configuration
2. CI/CD pipeline implementation and optimization
3. Monitoring and observability setup
4. Security automation and compliance
5. Deployment strategies and rollback procedures
6. Performance optimization and cost management

Focus on reliability, automation, and operational excellence.""",
            model=model,
        )

        output: DevOpsOutput = result.output

        # Framework-enforced output validation ensures structure
        if not output.worker:
            output.worker = worker
        if not output.session_id:
            output.session_id = session_id
        if not output.timestamp:
            output.timestamp = timestamp

        log_debug(
            session_id,
            "DevOps implementation completed",
            {
                "infrastructure_changes": len(output.infrastructure_changes),
                "deployment_strategies": len(output.deployment_strategies),
                "monitoring_implementations": len(output.monitoring_implementations),
                "infrastructure_maturity": output.infrastructure_maturity_score,
                "cicd_maturity": output.cicd_maturity_score,
                "observability_score": output.observability_score,
            },
        )

        # Create implementation files using protocol infrastructure
        create_devops_files(session_id, output)

        # Update session state to completed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "completed",
                f"{worker}_completed": timestamp,
                f"{worker}_infrastructure_maturity": output.infrastructure_maturity_score,
                f"{worker}_cicd_maturity": output.cicd_maturity_score,
                f"{worker}_observability": output.observability_score,
                f"{worker}_devops_maturity": output.devops_maturity_score,
            },
        )

        # Log completion
        log_event(
            session_id,
            "worker_completed",
            worker,
            {
                "duration": "calculated",
                "infrastructure_changes_count": len(output.infrastructure_changes),
                "deployment_strategies_count": len(output.deployment_strategies),
                "monitoring_implementations_count": len(
                    output.monitoring_implementations
                ),
                "status": output.status,
            },
        )

        return output

    except Exception as e:
        log_debug(
            session_id,
            "DevOps implementation failed",
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


def create_devops_files(session_id: str, output: DevOpsOutput):
    """Create DevOps output files using protocol infrastructure"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        notes_dir = session_path / "workers" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Create DevOps notes file if content provided
        if output.notes_markdown:
            notes_file = notes_dir / "devops_notes.md"
            notes_file.write_text(output.notes_markdown)
            log_debug(
                session_id, "Created DevOps notes file", {"path": str(notes_file)}
            )

        # Create structured output JSON
        output_file = notes_dir / "devops_output.json"
        output_file.write_text(output.model_dump_json(indent=2))
        log_debug(session_id, "Created DevOps output JSON", {"path": str(output_file)})

    except Exception as e:
        log_debug(session_id, "File creation failed", {"error": str(e)})


def main():
    """CLI entry point for DevOps worker"""
    parser = argparse.ArgumentParser(
        description="DevOps Worker - Infrastructure and Deployment"
    )
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument(
        "--task", required=True, help="DevOps implementation task description"
    )
    parser.add_argument("--model", default="openai:gpt-5", help="AI model to use")

    args = parser.parse_args()

    try:
        output = run_devops_implementation(args.session, args.task, args.model)
        print(
            f"DevOps implementation completed. Maturity score: {output.devops_maturity_score}, Infrastructure: {output.infrastructure_maturity_score}, CI/CD: {output.cicd_maturity_score}"
        )
        return 0
    except Exception as e:
        print(f"DevOps worker failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
