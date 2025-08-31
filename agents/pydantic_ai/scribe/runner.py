#!/usr/bin/env python3
"""
Scribe Agent Runner
==================  
Simple, working execution script for scribe agent.
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Add agents/pydantic_ai to path for imports
pydantic_ai_path = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, str(pydantic_ai_path))

from shared.protocols import (
    load_project_env,
    SessionManagement,
    LoggingProtocol,
    ProtocolConfig,
)

# Use helper function to load project environment
load_project_env()

# Direct imports
from pydantic_ai import Agent
from pydantic import BaseModel

# Import shared tools for consistency
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from tools import iso_now as shared_iso_now


class SessionCreation(BaseModel):
    session_id: str
    status: str
    timestamp: str
    task_description: str


def log_event(session_id: str, event_type: str, details: dict):
    """Log event using standardized protocol"""
    try:
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": "scribe"})
        logger = LoggingProtocol(cfg)
        logger.log_event(event_type, details)
    except Exception as e:
        print(f"Logging failed: {e}")


def log_debug(session_id: str, message: str, details: dict):
    """Log debug message using standardized protocol"""
    try:
        cfg = ProtocolConfig({"session_id": session_id, "agent_name": "scribe"})
        logger = LoggingProtocol(cfg)
        logger.log_debug(message, details)
    except Exception as e:
        print(f"Debug logging failed: {e}")


def update_session_state(session_id: str, state_update: dict):
    """Update session state - currently using direct file write until protocol adds this method"""
    try:
        # Get session path using SessionManagement
        project_root_path = Path(__file__).parent.parent.parent.parent.parent
        sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
        session_path = sessions_dir / session_id
        
        state_file = session_path / "STATE.json"
        with open(state_file, "w") as f:
            json.dump(state_update, f, indent=2)
            
        log_debug(session_id, "Session state updated", {"keys": list(state_update.keys())})
    except Exception as e:
        log_debug(session_id, "Session state update failed", {"error": str(e)})


def generate_ai_session_id(task_description: str, model: str) -> tuple[str, int]:
    """Generate session ID using AI to create better short description"""
    timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")

    # Check if API key is available - FAIL HARD if not
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError(
            "OPENAI_API_KEY environment variable is required for AI session ID generation"
        )

    # Use AI to generate a concise description
    class SessionDescription(BaseModel):
        short_name: str  # 1-3 words, lowercase, hyphens for spaces

    desc_agent = Agent(model, output_type=SessionDescription)

    prompt = f"""Create a very short description (1-3 words) for this task: {task_description}
    
    Requirements:
    - Maximum 3 words
    - Use lowercase
    - Use hyphens instead of spaces
    - Be descriptive but concise
    
    Examples:
    - "add user authentication" -> "user-auth"
    - "fix database connection issues" -> "db-fix"  
    - "implement payment processing" -> "payment-proc"
    """

    result = desc_agent.run_sync(prompt)
    short_desc = result.output.short_name
    # Clean and validate the description
    short_desc = re.sub(r"[^a-z0-9\-]", "", short_desc.lower())
    short_desc = re.sub(r"-+", "-", short_desc).strip("-")

    if len(short_desc) > 20:
        short_desc = short_desc[:20]

    session_id = f"{timestamp}-{short_desc}"
    return session_id, len(short_desc)


def create_session(task_description: str, model: str) -> dict:
    """Create a new session with directory structure"""

    session_id, desc_length = generate_ai_session_id(task_description, model)

    # Create session directory
    project_root_path = Path(__file__).parent.parent.parent.parent.parent
    sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
    session_path = sessions_dir / session_id

    session_path.mkdir(parents=True, exist_ok=True)
    (session_path / "workers").mkdir(exist_ok=True)
    (session_path / "workers" / "notes").mkdir(exist_ok=True)
    (session_path / "workers" / "prompts").mkdir(exist_ok=True)
    (session_path / "workers" / "json").mkdir(exist_ok=True)

    # Create session files using SessionManagement (which creates EVENTS.jsonl, DEBUG.jsonl, BACKLOG.jsonl)
    # The protocol infrastructure handles file creation
    events_file = session_path / "EVENTS.jsonl" 
    events_file.touch()
    debug_file = session_path / "DEBUG.jsonl"
    debug_file.touch()
    backlog_file = session_path / "BACKLOG.jsonl"
    backlog_file.touch()

    # Log session creation using standardized protocol
    log_event(session_id, "session_created", {
        "session_id": session_id,
        "task_description": task_description,
        "model": model,
        "session_path": f"Docs/hive-mind/sessions/{session_id}",
        "generated_by": "scribe",
        "description_length": desc_length,
    })

    # Log scribe spawn using standardized protocol  
    log_event(session_id, "worker_spawned", {
        "worker_type": "scribe",
        "mode": "create", 
        "model": model,
        "purpose": "session_creation",
    })

    # Create SESSION.md
    session_md_content = f"""# Session: {session_id}

**Created:** {shared_iso_now()}  
**Task:** {task_description}  
**Model:** {model}  
**Status:** Created  

## Overview
Session created for task analysis and worker coordination.

## Progress
- [x] Session initialization
- [ ] Task analysis  
- [ ] Worker deployment
- [ ] Synthesis

## Notes
Session ready for Queen orchestration.
"""

    with open(session_path / "SESSION.md", "w") as f:
        f.write(session_md_content)

    # Update session state using standardized protocol
    initial_state = {
        "session_id": session_id,
        "created": shared_iso_now(),
        "task_description": task_description,
        "model": model,
        "status": "created",
        "phase": "initialization",
        "workers": {
            "scribe": {
                "status": "active",
                "spawned_at": shared_iso_now(),
                "mode": "create",
            }
        },
    }
    
    update_session_state(session_id, initial_state)

    return {
        "session_id": session_id,
        "timestamp": shared_iso_now(),
        "status": "completed",
        "task_description": task_description,
        "complexity_level": 2,
        "session_path": f"Docs/hive-mind/sessions/{session_id}",
    }


def run_synthesis(session_id: str) -> dict:
    """Generate synthesis"""

    project_root_path = Path(__file__).parent.parent.parent.parent.parent
    sessions_dir = project_root_path / "Docs" / "hive-mind" / "sessions"
    session_path = sessions_dir / session_id

    if not session_path.exists():
        raise FileNotFoundError(f"Session {session_id} not found")

    synthesis = f"""# Synthesis - {session_id}

Generated: {shared_iso_now()}

## Summary
Session synthesis completed.

## Next Steps
Ready for worker coordination.
"""

    return {
        "session_id": session_id,
        "timestamp": shared_iso_now(),
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
