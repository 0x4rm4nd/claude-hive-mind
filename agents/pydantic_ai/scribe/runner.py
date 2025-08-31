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


def generate_ai_session_id(task_description: str, model: str) -> tuple[str, int]:
    """Generate session ID using AI to create better short description"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M')
    
    # Check if API key is available - FAIL HARD if not
    if not os.getenv('OPENAI_API_KEY'):
        raise ValueError("OPENAI_API_KEY environment variable is required for AI session ID generation")
    
    # Use AI to generate a concise description
    class SessionDescription(BaseModel):
        short_name: str  # 1-3 words, lowercase, hyphens for spaces
    
    desc_agent = Agent(model, result_type=SessionDescription)
    
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
    short_desc = result.data.short_name
    # Clean and validate the description
    short_desc = re.sub(r'[^a-z0-9\-]', '', short_desc.lower())
    short_desc = re.sub(r'-+', '-', short_desc).strip('-')
    
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
    (session_path / "prompts").mkdir(exist_ok=True)

    # Create EVENTS.jsonl
    events_file = session_path / "EVENTS.jsonl"
    events_file.touch()
    
    # Log session creation event
    session_created_event = {
        "timestamp": iso_now(),
        "event_type": "session_created",
        "worker_type": "scribe",
        "data": {
            "session_id": session_id,
            "task_description": task_description,
            "model": model,
            "session_path": str(session_path),
            "generated_by": "scribe",
            "description_length": desc_length
        }
    }
    with open(events_file, "a") as f:
        f.write(json.dumps(session_created_event) + "\n")
    
    # Log scribe spawn event
    worker_spawned_event = {
        "timestamp": iso_now(),
        "event_type": "worker_spawned", 
        "worker_type": "scribe",
        "data": {
            "worker_type": "scribe",
            "mode": "create",
            "model": model,
            "purpose": "session_creation"
        }
    }
    with open(events_file, "a") as f:
        f.write(json.dumps(worker_spawned_event) + "\n")

    # Create DEBUG.jsonl
    debug_file = session_path / "DEBUG.jsonl"
    debug_file.touch()
    
    # Create BACKLOG.jsonl
    backlog_file = session_path / "BACKLOG.jsonl"
    backlog_file.touch()

    # Create SESSION.md
    session_md_content = f"""# Session: {session_id}

**Created:** {iso_now()}  
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

    # Create complete STATE.json
    initial_state = {
        "session_id": session_id,
        "created": iso_now(),
        "task_description": task_description,
        "model": model,
        "status": "created",
        "phase": "initialization",
        "workers": {
            "scribe": {
                "status": "active",
                "spawned_at": iso_now(),
                "mode": "create"
            }
        }
    }

    with open(session_path / "STATE.json", "w") as f:
        json.dump(initial_state, f, indent=2)

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
