#!/usr/bin/env python3
import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from .deps import make_logger, HiveDeps
from .models import ScribeSynthesisOutput
from .agent_scribe import scribe_agent
from protocols.session_management import SessionManagement


def _iso_now() -> str:
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')


def _gather_worker_outputs(session_path: str) -> Dict[str, Any]:
    notes_dir = Path(session_path) / "notes"
    json_dir = Path(session_path) / "workers" / "json"

    notes_files = sorted([p for p in notes_dir.glob("*_notes.md") if p.is_file()])
    # exclude the final synthesis file if exists
    synthesis_file = notes_dir / "RESEARCH_SYNTHESIS.md"
    notes_files = [p for p in notes_files if p.name != "scribe_notes.md"]

    json_files = sorted([p for p in json_dir.glob("*_response.json") if p.is_file()])

    data = {
        "notes_files": [str(p) for p in notes_files],
        "json_files": [str(p) for p in json_files],
        "notes": {},
        "responses": {},
    }

    for p in notes_files:
        try:
            data["notes"][p.name] = p.read_text(encoding="utf-8")
        except Exception:
            data["notes"][p.name] = ""

    for p in json_files:
        try:
            data["responses"][p.name] = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            data["responses"][p.name] = {}

    return data


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def run(session_id: str, model: str) -> ScribeSynthesisOutput:
    if not SessionManagement.ensure_session_exists(session_id):
        raise SystemExit(f"Session does not exist or is invalid: {session_id}")

    session_path = SessionManagement.get_session_path(session_id)
    worker = "scribe-worker"
    logger = make_logger(session_id, worker)
    deps = HiveDeps(session_id=session_id, worker=worker, logger=logger)

    logger.log_event("worker_spawned", {"note": "Scribe activated for synthesis", "mode": "synthesis"})

    # Gather context deterministically and pass to the agent
    gathered = _gather_worker_outputs(session_path)

    # Compose user message (concise, structured context)
    user_msg = {
        "instruction": "Aggregate findings across workers and produce a synthesis.",
        "constraints": {
            "neutral": True,
            "no_new_claims": True,
            "cite_by_worker": True,
        },
        "files": {
            "notes_files": gathered["notes_files"],
            "json_files": gathered["json_files"],
        },
        "notes": gathered["notes"],
        "responses": gathered["responses"],
        "required_sections": [
            "Executive Summary",
            "Key Findings",
            "Consensus",
            "Conflicts",
            "Recommendations",
            "Evidence",
        ],
    }

    # Execute agent with model override if provided
    result = scribe_agent.run_sync(
        json.dumps(user_msg), deps=deps, model=model
    )
    out: ScribeSynthesisOutput = result.output

    # Deterministically write files
    sess = Path(session_path)
    # 1) Write research synthesis
    synthesis_path = sess / "notes" / "RESEARCH_SYNTHESIS.md"
    _write_text(synthesis_path, out.synthesis_markdown)
    logger.log_event("synthesis_created", {"file": str(synthesis_path)})

    logger.log_event("synthesis_completed", {"status": out.status})
    logger.log_event("session_completed", {"by": worker, "status": out.status})
    logger.log_event("worker_completed", {"status": out.status})

    return out


def main():
    parser = argparse.ArgumentParser(description="Run Pydantic AI scribe-worker (synthesis mode)")
    parser.add_argument("--session", required=True, help="Session ID")
    parser.add_argument(
        "--model",
        default=os.environ.get("PAI_MODEL", "openai:gpt-4o-mini"),
        help="Model provider:name, e.g., openai:gpt-4o-mini",
    )
    args = parser.parse_args()

    out = run(args.session, args.model)
    print(json.dumps(out.model_dump(), indent=2))


if __name__ == "__main__":
    main()
