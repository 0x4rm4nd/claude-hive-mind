"""
Unified Logging Functions Template
These are the authoritative logging functions for all agents.
DO NOT REIMPLEMENT - Reference from unified-logging-protocol.md
"""

import re
import json
from datetime import datetime

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
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
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

def log_event(session_id, event_type, agent_name, details, status=None):
    """ATOMIC APPEND to EVENTS.jsonl - Thread-safe implementation
    
    CRITICAL: session_id is ONLY used for file path, NOT included in event
    """
    from datetime import datetime
    import json
    
    # Generate timestamp in UTC ISO format
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    
    # Build event - NO session_id field in the event object
    event = {
        "timestamp": timestamp,
        "event_type": event_type,  # Standardized field name
        "worker": agent_name,  # Use 'worker' for consistency
        "details": str(details)[:500] if details else "No details provided"
    }
    
    if status:
        event["status"] = status
    
    # Serialize to JSON
    json_line = json.dumps(event, ensure_ascii=False)
    
    # ATOMIC APPEND using Bash echo
    events_file = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
    
    # Ensure directory exists
    Bash(f"mkdir -p Docs/hive-mind/sessions/{session_id}", description="Ensure session dir")
    
    # Atomic append
    escaped = json_line.replace("'", "'\"'\"'")
    Bash(f"echo '{escaped}' >> {events_file}", description=f"Log {event_type} event")
    
    print(f"✅ Event logged: {agent_name} - {event_type}")
    return True

def log_debug(session_id, level, agent_name, message, context=None):
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
    
    # ATOMIC APPEND using Bash echo
    debug_file = f"Docs/hive-mind/sessions/{session_id}/DEBUG.jsonl"
    
    # Atomic append
    escaped = json_line.replace("'", "'\"'\"'")
    Bash(f"echo '{escaped}' >> {debug_file}", description=f"Log {level} debug")
    
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

def verify_worker_compliance(session_id, worker_name):
    """Check if worker properly logged lifecycle events"""
    events = Read(f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl")
    
    required_events = [
        "worker_spawned",
        "session_validated", 
        "worker_configured",
        "analysis_started",  # No worker prefix
        "worker_completed"
    ]
    
    worker_events = []
    for line in events.strip().split('\n'):
        try:
            event = json.loads(line)
            if event.get("worker") == worker_name or event.get("agent") == worker_name:
                worker_events.append(event.get("event_type", event.get("type")))  # Support both field names
        except:
            continue
    
    missing = [e for e in required_events if e not in worker_events]
    
    if missing:
        log_debug(session_id, "WARNING", "queen-orchestrator", 
                 f"Worker {worker_name} missing events: {missing}")
    
    return len(missing) == 0
