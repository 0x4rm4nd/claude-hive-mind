"""
Analyzer Worker Runner
=====================
Execution script for analyzer worker with protocol compliance.
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

from .models import AnalyzerOutput
from .agent import analyzer_agent
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
        cfg = ProtocolConfig(
            {"session_id": session_id, "agent_name": "analyzer-worker"}
        )
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


def run_analyzer_analysis(
    session_id: str, task_description: str, model: str
) -> AnalyzerOutput:
    """Run analyzer worker with AI analysis"""
    worker = "analyzer-worker"
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
                "security_analysis",
                "performance_optimization",
                "code_quality_assessment",
                "dependency_analysis",
                "static_analysis",
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
                "analysis_type": "security_performance_quality",
                "timestamp": timestamp,
            },
        )

        # Execute analyzer agent
        result = analyzer_agent.run_sync(
            f"""Analyze the codebase for security vulnerabilities, performance issues, and code quality problems.

Task: {task_description}
Session: {session_id}

Perform comprehensive analysis including:
1. Security vulnerability assessment
2. Performance bottleneck identification  
3. Code quality metrics evaluation
4. Dependency security analysis
5. Technical debt quantification

Provide specific, actionable findings with clear priorities and effort estimates.""",
            model=model,
        )

        output: AnalyzerOutput = result.output

        # Framework-enforced output validation ensures structure
        if not output.worker:
            output.worker = worker
        if not output.session_id:
            output.session_id = session_id
        if not output.timestamp:
            output.timestamp = timestamp


        # Create analysis file using protocol infrastructure
        create_analyzer_files(session_id, output)

        # Update session state to completed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "completed",
                f"{worker}_completed": timestamp,
                f"{worker}_security_score": output.security_score,
                f"{worker}_performance_score": output.performance_score,
                f"{worker}_quality_score": output.quality_score,
            },
        )

        # Log completion
        log_event(
            session_id,
            "worker_completed",
            worker,
            {
                "duration": "calculated",
                "security_findings_count": len(output.security_findings),
                "performance_issues_count": len(output.performance_issues),
                "quality_metrics_count": len(output.quality_metrics),
                "status": output.status,
            },
        )

        return output

    except Exception as e:
        log_debug(
            session_id,
            "Analyzer analysis failed",
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


def create_analyzer_files(session_id: str, output: AnalyzerOutput):
    """Create analyzer output files using protocol infrastructure"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        notes_dir = session_path / "workers" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Create analyzer notes file if content provided
        if output.notes_markdown:
            notes_file = notes_dir / "analyzer_notes.md"
            notes_file.write_text(output.notes_markdown)
            log_debug(
                session_id, "Created analyzer notes file", {"path": str(notes_file)}
            )

        # Create structured output JSON
        output_file = notes_dir / "analyzer_output.json"
        output_file.write_text(output.model_dump_json(indent=2))
        log_debug(
            session_id, "Created analyzer output JSON", {"path": str(output_file)}
        )

    except Exception as e:
        log_debug(session_id, "File creation failed", {"error": str(e)}, "ERROR")


def main():
    """CLI entry point for analyzer worker"""
    parser = argparse.ArgumentParser(
        description="Analyzer Worker - Security and Performance Analysis"
    )
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--task", required=True, help="Analysis task description")
    parser.add_argument("--model", default="openai:gpt-5", help="AI model to use")

    args = parser.parse_args()

    try:
        output = run_analyzer_analysis(args.session, args.task, args.model)
        print(
            f"Analysis completed successfully. Security score: {output.security_score}, Performance score: {output.performance_score}, Quality score: {output.quality_score}"
        )
        return 0
    except Exception as e:
        print(f"Analyzer failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
