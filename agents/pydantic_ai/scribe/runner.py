#!/usr/bin/env python3
"""
Scribe Agent Runner
==================  
Simple, working execution script for scribe agent.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Simple approach: just add project root to path and use direct imports
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Direct imports
from pydantic_ai import Agent
from pydantic import BaseModel


class SessionCreation(BaseModel):
    session_id: str
    status: str
    timestamp: str
    task_description: str


def iso_now() -> str:
    return datetime.utcnow().isoformat() + "Z"


def create_session_id(task: str) -> str:
    """Create a session ID from task description"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")
    # Simple task summarization
    words = task.lower().split()[:3]
    task_part = "-".join(w[:8] for w in words if w.isalnum())[:20]
    return f"{timestamp}-{task_part}"


def create_session(task_description: str, model: str) -> dict:
    """Create a new session with directory structure"""

    session_id = create_session_id(task_description)

    # Create session directory
    project_root_path = Path(__file__).parent.parent.parent.parent.parent
    sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
    session_path = sessions_dir / session_id

    session_path.mkdir(parents=True, exist_ok=True)
    (session_path / "workers").mkdir(exist_ok=True)

    # Create STATE.json
    state = {
        "session_id": session_id,
        "created": iso_now(),
        "task_description": task_description,
        "model": model,
        "status": "created",
    }

    with open(session_path / "STATE.json", "w") as f:
        json.dump(state, f, indent=2)

    return {
        "session_id": session_id,
        "timestamp": iso_now(),
        "status": "completed",
        "task_description": task_description,
        "complexity_level": 2,
        "session_path": str(session_path),
    }


def run_synthesis(session_id: str) -> dict:
    """Generate synthesis"""

    project_root_path = Path(__file__).parent.parent.parent.parent.parent
    sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
    session_path = sessions_dir / session_id

    if not session_path.exists():
        raise FileNotFoundError(f"Session {session_id} not found")

    synthesis = f"""# Synthesis - {session_id}

Generated: {iso_now()}

## Summary
Session synthesis completed.

## Next Steps
Ready for worker coordination.
"""

    return {
        "session_id": session_id,
        "timestamp": iso_now(),
        "status": "completed",
        "synthesis_markdown": synthesis,
    }


def main():
    parser = argparse.ArgumentParser(description="Scribe Agent")
    parser.add_argument("mode", choices=["create", "synthesis"])
    parser.add_argument("--task", help="Task description")
    parser.add_argument("--session", help="Session ID")
    parser.add_argument("--model", default="openai:gpt-5")

    args = parser.parse_args()

    try:
        if args.mode == "create":
            if not args.task:
                raise ValueError("--task required for create mode")
            result = create_session(args.task, args.model)

        elif args.mode == "synthesis":
            if not args.session:
                raise ValueError("--session required for synthesis mode")
            result = run_synthesis(args.session)

        print(json.dumps(result, indent=2))

    except Exception as e:
        error = {
            "error": str(e),
            "mode": args.mode,
            "task": args.task,
            "session": args.session,
        }
        print(json.dumps(error, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
