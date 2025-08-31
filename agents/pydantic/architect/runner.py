"""
Architect Worker Runner
======================
Execution script for architect worker with protocol compliance.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import sys
import os

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from protocols import (
    SessionManagement,
    LoggingProtocol,
    ProtocolConfig,
    WorkerPromptProtocol,
)

from .models import ArchitectOutput
from .agent import architect_agent
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
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": "architect-worker"})
        logger = LoggingProtocol(cfg)
        logger.log_debug(message, details)
    except Exception as e:
        print(f"Debug logging failed: {e}")


def update_session_state(session_id: str, state_update: Dict[str, Any]):
    """Update session state using protocol infrastructure"""
    try:
        SessionManagement.update_session_state(session_id, state_update)
        log_debug(session_id, "Session state updated", {"keys": list(state_update.keys())})
    except Exception as e:
        log_debug(session_id, "Session state update failed", {"error": str(e)})


def run_architect_analysis(
    session_id: str, task_description: str, model: str
) -> ArchitectOutput:
    """Run architect worker with AI analysis"""
    worker = "architect-worker"
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
                "system_architecture",
                "scalability_patterns",
                "design_patterns",
                "technology_evaluation",
                "api_design"
            ]
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
        log_debug(session_id, "Starting architect analysis", {"task": task_description})
        
        # Execute architect agent
        result = architect_agent.run_sync(
            f"""Analyze the system architecture and provide design recommendations.

Task: {task_description}
Session: {session_id}

Perform comprehensive architectural analysis including:
1. Current architecture assessment and pattern recognition
2. Scalability evaluation and bottleneck identification
3. Technology decisions and stack evaluation
4. Design pattern application and SOLID principles adherence
5. Integration pattern analysis and API design review
6. Evolution roadmap and modernization opportunities

Focus on strategic, high-impact architectural improvements with clear implementation priorities.""",
            model=model
        )

        output: ArchitectOutput = result.output

        # Framework-enforced output validation ensures structure
        if not output.worker:
            output.worker = worker
        if not output.session_id:
            output.session_id = session_id
        if not output.timestamp:
            output.timestamp = timestamp

        log_debug(
            session_id,
            "Architect analysis completed",
            {
                "architectural_recommendations": len(output.architectural_recommendations),
                "technology_decisions": len(output.technology_decisions),
                "architectural_maturity_score": output.architectural_maturity_score,
                "architecture_quality_score": output.architecture_quality_score,
                "maintainability_score": output.maintainability_score,
                "extensibility_score": output.extensibility_score
            },
        )

        # Create analysis file using protocol infrastructure
        create_architect_files(session_id, output)

        # Update session state to completed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "completed",
                f"{worker}_completed": timestamp,
                f"{worker}_architectural_maturity": output.architectural_maturity_score,
                f"{worker}_architecture_quality": output.architecture_quality_score,
                f"{worker}_maintainability": output.maintainability_score,
                f"{worker}_extensibility": output.extensibility_score,
            },
        )

        # Log completion
        log_event(
            session_id,
            "worker_completed",
            worker,
            {
                "duration": "calculated",
                "recommendations_count": len(output.architectural_recommendations),
                "technology_decisions_count": len(output.technology_decisions),
                "status": output.status,
            },
        )

        return output

    except Exception as e:
        log_debug(
            session_id, "Architect analysis failed", {"error": str(e), "task": task_description}
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

        # Log failure
        log_event(
            session_id,
            "worker_failed",
            worker,
            {"error": str(e), "task": task_description},
        )
        
        raise


def create_architect_files(session_id: str, output: ArchitectOutput):
    """Create architect output files using protocol infrastructure"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        notes_dir = session_path / "workers" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Create architect notes file if content provided
        if output.notes_markdown:
            notes_file = notes_dir / "architect_notes.md"
            notes_file.write_text(output.notes_markdown)
            log_debug(session_id, "Created architect notes file", {"path": str(notes_file)})

        # Create structured output JSON
        output_file = notes_dir / "architect_output.json"
        output_file.write_text(output.model_dump_json(indent=2))
        log_debug(session_id, "Created architect output JSON", {"path": str(output_file)})

    except Exception as e:
        log_debug(session_id, "File creation failed", {"error": str(e)})


def main():
    """CLI entry point for architect worker"""
    parser = argparse.ArgumentParser(description="Architect Worker - System Design and Architecture Analysis")
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--task", required=True, help="Architecture task description")
    parser.add_argument("--model", default="openai:gpt-4o-mini", help="AI model to use")
    
    args = parser.parse_args()
    
    try:
        output = run_architect_analysis(args.session, args.task, args.model)
        print(f"Architecture analysis completed. Quality score: {output.architecture_quality_score}, Maintainability: {output.maintainability_score}, Extensibility: {output.extensibility_score}")
        return 0
    except Exception as e:
        print(f"Architect failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())