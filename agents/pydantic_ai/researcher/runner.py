"""
Researcher Worker Runner
=======================
Execution script for researcher worker with protocol compliance.
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

from .models import ResearcherOutput
from .agent import researcher_agent
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
    """Log message using protocol infrastructure with specified level"""
    try:
        cfg = ProtocolConfig(
            {"session_id": session_id, "agent_name": "researcher-worker"}
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


def run_researcher_analysis(
    session_id: str, task_description: str, model: str
) -> ResearcherOutput:
    """Run researcher worker with AI analysis"""
    worker = "researcher-worker"
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
                "technical_research",
                "technology_evaluation",
                "best_practices_analysis",
                "industry_standards",
                "competitive_intelligence",
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
                "analysis_type": "research_analysis",
                "timestamp": timestamp,
            },
        )

        # Execute researcher agent
        result = researcher_agent.run_sync(
            f"""Conduct comprehensive technical research and analysis.

Task: {task_description}
Session: {session_id}

Perform thorough research analysis including:
1. Technology evaluation and comparison
2. Industry best practices and standards research
3. Security and compliance requirements analysis
4. Performance optimization insights and benchmarks
5. Emerging technology trends and adoption considerations
6. Competitive analysis and market intelligence

Focus on evidence-based findings with credible sources and actionable recommendations.""",
            model=model,
        )

        output: ResearcherOutput = result.output

        # Framework-enforced output validation ensures structure
        if not output.worker:
            output.worker = worker
        if not output.session_id:
            output.session_id = session_id
        if not output.timestamp:
            output.timestamp = timestamp


        # Create research files using protocol infrastructure
        create_researcher_files(session_id, output)

        # Update session state to completed
        update_session_state(
            session_id,
            {
                f"{worker}_status": "completed",
                f"{worker}_completed": timestamp,
                f"{worker}_research_depth": output.research_depth_score,
                f"{worker}_source_credibility": output.source_credibility_score,
                f"{worker}_relevance": output.relevance_score,
                f"{worker}_research_quality": output.research_quality_score,
            },
        )

        # Log completion
        log_event(
            session_id,
            "worker_completed",
            worker,
            {
                "duration": "calculated",
                "research_findings_count": len(output.research_findings),
                "technology_evaluations_count": len(output.technology_evaluations),
                "best_practices_count": len(output.best_practice_recommendations),
                "status": output.status,
            },
        )

        return output

    except Exception as e:
        log_debug(
            session_id,
            "Research analysis failed",
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


def create_researcher_files(session_id: str, output: ResearcherOutput):
    """Create researcher output files using protocol infrastructure"""
    try:
        session_path = SessionManagement.get_session_path(session_id)
        notes_dir = session_path / "workers" / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        # Create researcher notes file if content provided
        if output.notes_markdown:
            notes_file = notes_dir / "researcher_notes.md"
            notes_file.write_text(output.notes_markdown)
            log_debug(
                session_id, "Created researcher notes file", {"path": str(notes_file)}
            )

        # Create structured output JSON
        output_file = notes_dir / "researcher_output.json"
        output_file.write_text(output.model_dump_json(indent=2))
        log_debug(
            session_id, "Created researcher output JSON", {"path": str(output_file)}
        )

    except Exception as e:
        log_debug(session_id, "File creation failed", {"error": str(e)}, "ERROR")


def main():
    """CLI entry point for researcher worker"""
    parser = argparse.ArgumentParser(
        description="Researcher Worker - Technical Research and Analysis"
    )
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument("--task", required=True, help="Research task description")
    parser.add_argument("--model", default="openai:gpt-5", help="AI model to use")

    args = parser.parse_args()

    try:
        output = run_researcher_analysis(args.session, args.task, args.model)
        print(
            f"Research analysis completed. Quality score: {output.research_quality_score}, Depth: {output.research_depth_score}, Relevance: {output.relevance_score}"
        )
        return 0
    except Exception as e:
        print(f"Researcher worker failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
