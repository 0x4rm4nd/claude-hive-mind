"""
Test Worker Runner
=================
Execution script for test worker with protocol compliance.
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

from .models import TestOutput
from .agent import test_agent
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
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": "test-worker"})
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


def run_test_implementation(
    session_id: str, task_description: str, model: str
) -> TestOutput:
    """Run test worker with AI implementation"""
    worker = "test-worker"
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
                "test_strategy_design",
                "test_automation",
                "quality_assurance",
                "coverage_analysis",
                "performance_testing",
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
            session_id, "Starting test implementation", {"task": task_description}
        )
        
        # Log analysis started event for behavior tracking
        log_event(
            session_id,
            "analysis_started",
            worker,
            {
                "task": task_description,
                "analysis_type": "test_implementation",
                "timestamp": timestamp,
            },
        )

        # Execute test agent
        result = test_agent.run_sync(
            f"""Design and implement comprehensive testing strategies and implementations.

Task: {task_description}
Session: {session_id}

Perform comprehensive testing analysis including:
1. Test strategy design and framework selection
2. Test implementation planning and coverage analysis
3. Quality gate definition and automation integration
4. Performance testing strategy and load testing
5. Security testing approach and vulnerability validation
6. Accessibility testing and WCAG compliance verification

Focus on comprehensive quality assurance with automated testing and continuous validation.""",
            model=model,
        )

        output: TestOutput = result.output

        # Framework-enforced output validation ensures structure
        if not output.worker:
            output.worker = worker
        if not output.session_id:
            output.session_id = session_id
        if not output.timestamp:
            output.timestamp = timestamp

        log_debug(
            session_id,
            "Test implementation completed",
            {
                "test_implementations": len(output.test_implementations),
                "testing_strategies": len(output.testing_strategies),
                "quality_gates": len(output.quality_gates),
                "test_implementation_score": output.test_implementation_score,
                "testing_maturity_score": output.testing_maturity_score,
                "overall_test_quality_score": output.overall_test_quality_score,
            },
        )

        # Create test files using protocol infrastructure
        create_test_files(session_id, output)

        # Update session state to completed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "completed",
                f"{worker}_completed": timestamp,
                f"{worker}_test_implementation": output.test_implementation_score,
                f"{worker}_testing_maturity": output.testing_maturity_score,
                f"{worker}_test_quality": output.overall_test_quality_score,
                f"{worker}_defect_prevention": output.defect_prevention_score,
            },
        )

        # Log completion
        log_event(
            session_id,
            "worker_completed",
            worker,
            {
                "duration": "calculated",
                "test_implementations_count": len(output.test_implementations),
                "testing_strategies_count": len(output.testing_strategies),
                "quality_gates_count": len(output.quality_gates),
                "status": output.status,
            },
        )

        return output

    except Exception as e:
        log_debug(
            session_id,
            "Test implementation failed",
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


def create_test_files(session_id: str, output: TestOutput):
    """Create test output files using protocol infrastructure"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        notes_dir = session_path / "workers" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Create test notes file if content provided
        if output.notes_markdown:
            notes_file = notes_dir / "test_notes.md"
            notes_file.write_text(output.notes_markdown)
            log_debug(session_id, "Created test notes file", {"path": str(notes_file)})

        # Create structured output JSON
        output_file = notes_dir / "test_output.json"
        output_file.write_text(output.model_dump_json(indent=2))
        log_debug(session_id, "Created test output JSON", {"path": str(output_file)})

    except Exception as e:
        log_debug(session_id, "File creation failed", {"error": str(e)})


def main():
    """CLI entry point for test worker"""
    parser = argparse.ArgumentParser(
        description="Test Worker - Testing Strategy and Quality Assurance"
    )
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--task", required=True, help="Testing task description")
    parser.add_argument("--model", default="openai:gpt-5", help="AI model to use")

    args = parser.parse_args()

    try:
        output = run_test_implementation(args.session, args.task, args.model)
        print(
            f"Test implementation completed. Quality score: {output.overall_test_quality_score}, Maturity: {output.testing_maturity_score}, Defect prevention: {output.defect_prevention_score}"
        )
        return 0
    except Exception as e:
        print(f"Test worker failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
