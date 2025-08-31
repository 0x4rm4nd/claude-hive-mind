"""
Scribe Runner
============
Session creation and synthesis execution.
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

import sys

# Environment setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))

from ..shared.protocols import SessionManagement

from .models import ScribeSynthesisOutput, ScribeSessionCreationOutput, TaskSummaryOutput
from .agent import task_summary_agent
from ..shared.tools import iso_now, detect_project_root


def generate_ai_session_id(task_description: str, model: str) -> tuple[str, int]:
    """Generate session ID using AI to create better short description"""
    timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M')
    
    if task_summary_agent:
        try:
            # Use AI to generate better short description
            result = task_summary_agent.run_sync(
                f"Task: {task_description}", 
                model=model
            )
            summary: TaskSummaryOutput = result.output
            
            short_desc = summary.short_description.lower().replace('_', '-')
            # Ensure it's properly hyphenated and not too long
            if len(short_desc) > 50:
                short_desc = short_desc[:50].rstrip('-')
            
            session_id = f"{timestamp}-{short_desc}"
            return session_id, summary.complexity_level
            
        except Exception as e:
            print(f"AI summary failed, using fallback: {e}")
    
    # Fallback to smart slugification
    return generate_smart_session_id(task_description, timestamp)


def generate_smart_session_id(task_description: str, timestamp: str) -> tuple[str, int]:
    """Smart session ID generation without AI"""
    
    # Enhanced rules for better session IDs
    task_lower = task_description.lower()
    
    # Domain-specific keywords mapping
    domain_map = {
        'crypto': 'crypto',
        'security': 'security', 
        'performance': 'perf',
        'analyze': 'analysis',
        'review': 'review',
        'audit': 'audit',
        'implement': 'impl',
        'optimize': 'opt',
        'fix': 'fix',
        'bug': 'bugfix',
        'api': 'api',
        'database': 'db',
        'frontend': 'fe',
        'backend': 'be',
        'microservice': 'svc',
        'architecture': 'arch',
        'deploy': 'deploy',
        'test': 'test'
    }
    
    # Extract meaningful words and map to shorter versions
    words = re.findall(r'\\b[a-zA-Z0-9]+\\b', task_lower)
    mapped_words = []
    
    for word in words:
        if word in domain_map:
            mapped_words.append(domain_map[word])
        elif len(word) > 3 and word not in {'the', 'and', 'for', 'with', 'from', 'this', 'that'}:
            mapped_words.append(word)
    
    # Take first 3-4 meaningful words
    meaningful_words = mapped_words[:4] if len(mapped_words) >= 2 else words[:3]
    
    task_slug = '-'.join(meaningful_words) if meaningful_words else 'task'
    if len(task_slug) > 50:
        task_slug = task_slug[:50].rstrip('-')
    
    # Smart complexity assessment
    complexity_indicators = {
        'architecture': 4, 'comprehensive': 4, 'full': 3, 'complete': 3,
        'security': 3, 'performance': 3, 'scalability': 3, 
        'analyze': 2, 'review': 2, 'audit': 3,
        'implement': 2, 'create': 2, 'build': 2,
        'fix': 1, 'update': 1, 'simple': 1
    }
    
    max_complexity = 1
    for word in words:
        if word in complexity_indicators:
            max_complexity = max(max_complexity, complexity_indicators[word])
    
    # Also consider length
    length_complexity = min(4, len(task_description.split()) // 8 + 1)
    complexity = max(max_complexity, length_complexity)
    
    session_id = f"{timestamp}-{task_slug}"
    return session_id, complexity


def log_event(session_id: str, event_type: str, agent: str, details: Any):
    """Simple event logging to EVENTS.jsonl"""
    timestamp = iso_now()
    event = {
        "timestamp": timestamp,
        "type": event_type,
        "agent": agent,
        "details": details
    }
    
    # Find session directory
    project_root = detect_project_root()
    events_file = Path(project_root) / "Docs" / "hive-mind" / "sessions" / session_id / "EVENTS.jsonl"
    
    # Append to events file
    with open(events_file, 'a') as f:
        f.write(json.dumps(event) + '\\n')


def create_session(task_description: str, model: str) -> ScribeSessionCreationOutput:
    """Create a new session with proper structure"""
    
    # Use AI to generate better session ID and complexity assessment
    session_id, complexity = generate_ai_session_id(task_description, model)
    worker = "scribe-worker"
    
    # Create session directory structure
    project_root = detect_project_root()
    session_path = Path(project_root) / "Docs" / "hive-mind" / "sessions" / session_id
    
    # Create directories
    session_path.mkdir(parents=True, exist_ok=True)
    (session_path / "workers" / "notes").mkdir(parents=True, exist_ok=True)
    (session_path / "workers" / "json").mkdir(parents=True, exist_ok=True)
    (session_path / "prompts").mkdir(exist_ok=True)
    
    timestamp = iso_now()
    
    # Create STATE.json
    initial_state = {
        "session_id": session_id,
        "task": task_description,
        "complexity_level": complexity,
        "created_at": timestamp,
        "status": "initialized",
        "active_workers": [],
        "worker_configs": {},
        "completion_status": {}
    }
    
    with open(session_path / "STATE.json", 'w') as f:
        json.dump(initial_state, f, indent=2)
    
    # Create SESSION.md
    session_md = f"""# Session: {session_id}

## Task
{task_description}

## Configuration
- **Created**: {timestamp}
- **Complexity Level**: {complexity}
- **Status**: Initialized

## Directory Structure
- `STATE.json` - Session state and worker tracking
- `EVENTS.jsonl` - Event logging stream
- `workers/notes/` - Human-readable analysis outputs  
- `workers/json/` - Machine-readable worker responses
- `prompts/` - Worker-specific task instructions
"""
    
    with open(session_path / "SESSION.md", 'w') as f:
        f.write(session_md)
    
    # Initialize empty files
    (session_path / "EVENTS.jsonl").touch()
    (session_path / "DEBUG.jsonl").touch()
    (session_path / "BACKLOG.jsonl").touch()
    
    # Log events
    log_event(session_id, "worker_spawned", worker, {"note": "Scribe activated for session creation", "mode": "creation"})
    log_event(session_id, "session_created", worker, {
        "session_id": session_id,
        "task": task_description,
        "complexity_level": complexity,
        "session_path": str(session_path)
    })
    
    return ScribeSessionCreationOutput(
        session_id=session_id,
        timestamp=timestamp,
        status="completed",
        task_description=task_description,
        complexity_level=complexity,
        session_path=str(session_path)
    )


def run_synthesis(session_id: str, model: str) -> ScribeSynthesisOutput:
    """Run synthesis on completed worker outputs"""
    
    project_root = detect_project_root()
    session_path = Path(project_root) / "Docs" / "hive-mind" / "sessions" / session_id
    
    if not session_path.exists():
        raise SystemExit(f"Session does not exist: {session_id}")
    
    worker = "scribe-worker"
    timestamp = iso_now()
    
    # Log worker spawn
    log_event(session_id, "worker_spawned", worker, {"note": "Scribe activated for synthesis", "mode": "synthesis"})
    
    # Simple synthesis for now (no AI needed for basic functionality test)
    synthesis_md = f"""# Research Synthesis

## Session: {session_id}
**Generated**: {timestamp}

## Executive Summary
This synthesis was generated by the Pydantic AI scribe worker.

## Key Findings
- Session processed successfully
- Basic synthesis functionality working

## Recommendations  
- System is operational
- Ready for full AI-powered synthesis

---
*Generated by Pydantic AI scribe-worker*
"""
    
    # Write synthesis file
    synthesis_path = session_path / "workers" / "notes" / "RESEARCH_SYNTHESIS.md"
    synthesis_path.write_text(synthesis_md, encoding="utf-8")
    
    # Log completion
    log_event(session_id, "synthesis_created", worker, {"file": str(synthesis_path)})
    log_event(session_id, "synthesis_completed", worker, {"status": "completed"})
    log_event(session_id, "session_completed", worker, {"by": worker, "status": "completed"})
    log_event(session_id, "worker_completed", worker, {"status": "completed"})
    
    return ScribeSynthesisOutput(
        session_id=session_id,
        timestamp=timestamp,
        status="completed",
        synthesis_markdown=synthesis_md
    )


def main():
    parser = argparse.ArgumentParser(description="Pydantic AI scribe-worker")
    parser.add_argument(
        "mode", 
        choices=["create", "synthesis"], 
        help="Mode: 'create' for session creation, 'synthesis' for final synthesis"
    )
    parser.add_argument("--session", help="Session ID (required for synthesis mode)")
    parser.add_argument("--task", help="Task description (required for create mode)")
    parser.add_argument("--model", default="openai:gpt-4o-mini", help="Model (not used in basic version)")
    
    args = parser.parse_args()

    if args.mode == "create":
        if not args.task:
            parser.error("--task is required for create mode")
        out = create_session(args.task, args.model)
        print(json.dumps(out.model_dump(), indent=2))
    
    elif args.mode == "synthesis":
        if not args.session:
            parser.error("--session is required for synthesis mode")  
        out = run_synthesis(args.session, args.model)
        print(json.dumps(out.model_dump(), indent=2))


if __name__ == "__main__":
    main()