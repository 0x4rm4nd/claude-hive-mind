"""
Unified Logging Functions Template
These are the authoritative logging functions for all agents.
DO NOT REIMPLEMENT - Reference from unified-logging-protocol.md
"""

import re
import os
import json
from datetime import datetime
from typing import Any

def _atomic_append(file_path: str, json_line: str) -> None:
    """Atomically append a JSON line to a file using O_APPEND and fsync.

    - Ensures directory exists
    - Uses O_CREAT|O_APPEND|O_WRONLY to prevent truncation
    - Attempts to acquire an advisory flock if available (best-effort)
    """
    # Ensure parent directory exists
    parent = os.path.dirname(file_path)
    if parent and not os.path.exists(parent):
        os.makedirs(parent, exist_ok=True)

    flags = os.O_CREAT | os.O_APPEND | os.O_WRONLY
    fd = os.open(file_path, flags, 0o644)
    try:
        # Best-effort advisory file lock
        try:
            import fcntl  # type: ignore
            fcntl.flock(fd, fcntl.LOCK_EX)
        except Exception:
            pass  # If flock unavailable, continue without it

        # Ensure a newline after the JSON line
        data = (json_line.rstrip("\n") + "\n").encode("utf-8")
        os.write(fd, data)
        os.fsync(fd)
    finally:
        try:
            # Best-effort unlock
            try:
                import fcntl  # type: ignore
                fcntl.flock(fd, fcntl.LOCK_UN)
            except Exception:
                pass
            os.close(fd)
        except Exception:
            pass

# MANDATORY: Extract session ID at agent start
def extract_session_id(prompt_text, worker_type):
    """Universal session extraction - MUST be first operation"""
    if "Session ID:" in prompt_text:
        match = re.search(r"Session ID:\s*([^\s\n-]+)", prompt_text)
        session_id = match.group(1).strip() if match else None
    elif "session_id" in prompt_text.lower():
        match = re.search(r"session[_\s]?id[:\s]+([^\s\n,]+)", prompt_text, re.IGNORECASE)
        session_id = match.group(1).strip() if match else None
    else:
        # Fallback: Generate from context
        task_slug = re.sub(r'[^a-zA-Z0-9]+', '-', prompt_text[:100].lower())[:50]
        from datetime import datetime
        timestamp = datetime.utcnow().strftime('%Y-%m-%d-%H-%M')
        session_id = f"{timestamp}-{task_slug}"
    
    # Validate session path exists
    session_path = f"Docs/hive-mind/sessions/{session_id}"
    try:
        state_content = Read(f"{session_path}/STATE.json")
        if not state_content:
            raise Exception(f"Session {session_id} STATE.json is empty")
    except:
        raise Exception(f"FATAL: Session {session_id} not found at {session_path}")
    
    return session_id

def log_event(session_id: str, event_type: str, agent_name: str, details: Any, status: str | None = None):
    """ATOMIC APPEND to EVENTS.jsonl - Thread-safe implementation
    
    CRITICAL: session_id is ONLY used for file path, NOT included in event
    """
    from datetime import datetime
    import json
    
    # Generate timestamp in UTC ISO format
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Build event - NO session_id field in the event object
    # Standardize field names to match schema: type + agent
    event = {
        "timestamp": timestamp,
        "type": event_type,
        "agent": agent_name,
        "details": str(details)[:500] if details else "No details provided"
    }
    
    if status:
        event["status"] = status
    
    # Serialize to JSON
    json_line = json.dumps(event, ensure_ascii=False)
    
    # Atomic append to EVENTS.jsonl
    events_file = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
    _atomic_append(events_file, json_line)
    
    print(f"✅ Event logged: {agent_name} - {event_type}")
    return True

def log_debug(session_id: str, level: str, agent_name: str, message: str, context: Any | None = None):
    """ATOMIC APPEND to DEBUG.jsonl - Thread-safe implementation"""
    from datetime import datetime
    import json
    
    # Generate timestamp in UTC ISO format
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Build debug entry - no session_path field
    debug_entry = {
        "timestamp": timestamp,
        "level": level,  # INFO, SUCCESS, WARNING, ERROR, COMPLIANCE
        "agent": agent_name,
        "message": str(message)[:1000]
    }
    
    if context:
        debug_entry["context"] = context
    
    # Serialize to JSON
    json_line = json.dumps(debug_entry, ensure_ascii=False)
    
    # Atomic append to DEBUG.jsonl
    debug_file = f"Docs/hive-mind/sessions/{session_id}/DEBUG.jsonl"
    _atomic_append(debug_file, json_line)
    return True

def check_my_compliance(session_id, worker_type):
    """Self-check for protocol compliance"""
    try:
        events = Read(f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl")
        my_events = [json.loads(line) for line in events.strip().split('\n') 
                     if worker_type in line]
        
        print(f"📊 Total events logged: {len(my_events)}")
        print(f"✅ Compliance status: {'PASS' if len(my_events) >= 5 else 'FAIL'}")
        
        return len(my_events) >= 5
    except:
        print("❌ Compliance check failed - no events found")
        return False

def verify_worker_compliance(session_id: str, worker_name: str) -> bool:
    """Check worker lifecycle compliance and output files.

    Asserts:
    - First event for the worker is worker_spawned
    - Required events present
    - Both output files exist (notes and JSON response)
    """
    events_path = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
    lines: list[str] = []
    try:
        with open(events_path, "r", encoding="utf-8") as f:
            lines = f.read().strip().split("\n") if f.readable() else []
    except Exception:
        lines = []

    required_events = [
        "worker_spawned",
        "session_validated",
        "worker_configured",
        "analysis_started",
        "worker_completed",
    ]

    worker_event_types: list[str] = []
    first_event_type: str | None = None

    for raw in lines:
        if not raw:
            continue
        try:
            evt = json.loads(raw)
        except Exception:
            continue
        agent_name = evt.get("agent") or evt.get("worker")
        if agent_name != worker_name:
            continue
        evt_type = evt.get("type") or evt.get("event_type")
        if first_event_type is None:
            first_event_type = evt_type
        if evt_type:
            worker_event_types.append(evt_type)

    missing = [e for e in required_events if e not in worker_event_types]
    first_ok = first_event_type == "worker_spawned"

    # Output files check
    worker_type_clean = worker_name.replace("-worker", "")
    session_root = f"Docs/hive-mind/sessions/{session_id}"
    notes_path = os.path.join(session_root, "workers", f"{worker_type_clean}_notes.md")
    json_path = os.path.join(session_root, "workers", "json", f"{worker_type_clean}_response.json")
    notes_ok = os.path.exists(notes_path)
    json_ok = os.path.exists(json_path)

    ok = (not missing) and first_ok and notes_ok and json_ok

    if not ok:
        problems = {
            "missing_events": missing,
            "first_event": first_event_type,
            "notes_exists": notes_ok,
            "json_exists": json_ok,
        }
        try:
            log_debug(session_id, "COMPLIANCE", "queen-orchestrator", f"Compliance check failed for {worker_name}", problems)
        except Exception:
            pass
    else:
        try:
            log_debug(session_id, "COMPLIANCE", "queen-orchestrator", f"Compliance passed for {worker_name}")
        except Exception:
            pass

    return ok
