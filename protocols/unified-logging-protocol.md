# 🔐 Unified Logging Protocol - Single Source of Truth

## Purpose
**THE AUTHORITATIVE LOGGING STANDARD** - All agents MUST use these exact functions for EVENTS.jsonl and DEBUG.jsonl logging. This protocol supersedes all other logging implementations.

## ⚠️ CRITICAL REQUIREMENTS
1. **NO INLINE IMPLEMENTATIONS** - Agents must NOT implement their own logging
2. **REFERENCE ONLY** - Agents must reference this protocol file
3. **EXACT FUNCTION USAGE** - Use the exact function signatures below
4. **MANDATORY LOGGING** - All lifecycle events MUST be logged

## 📋 Universal Session Extraction (Step 1 for ALL Agents)

```python
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
```

## 🎯 EVENTS.jsonl Logging Function (Universal)

```python
def log_event(session_id, event_type, agent_name, details, status=None):
    """ATOMIC APPEND to EVENTS.jsonl - Thread-safe implementation"""
    from datetime import datetime
    import json
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+02:00')
    
    # Build event
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
    
    # ATOMIC APPEND using Bash echo
    events_file = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
    
    # Ensure directory exists
    Bash(f"mkdir -p Docs/hive-mind/sessions/{session_id}", description="Ensure session dir")
    
    # Atomic append
    escaped = json_line.replace("'", "'\"'\"'")
    Bash(f"echo '{escaped}' >> {events_file}", description=f"Log {event_type} event")
    
    print(f"✅ Event logged: {agent_name} - {event_type}")
    return True
```

## 🐛 DEBUG.jsonl Logging Function (Universal)

```python
def log_debug(session_id, level, agent_name, message, context=None):
    """ATOMIC APPEND to DEBUG.jsonl - Thread-safe implementation"""
    from datetime import datetime
    import json
    
    # Generate timestamp
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S+02:00')
    
    # Build debug entry
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
```

## 🚀 Mandatory Worker Startup Sequence

**EVERY WORKER MUST EXECUTE IN THIS EXACT ORDER:**

```python
# Step 1: Extract Session
session_id = extract_session_id(prompt, WORKER_TYPE)
log_debug(session_id, "INFO", WORKER_TYPE, f"Session ID extracted: {session_id}")

# Step 2: Log Spawn Event
log_event(session_id, "worker_spawned", WORKER_TYPE, f"{WORKER_TYPE} activated")
log_debug(session_id, "INFO", WORKER_TYPE, "Worker spawn logged")

# Step 3: Validate Session State
state = json.loads(Read(f"Docs/hive-mind/sessions/{session_id}/STATE.json"))
worker_config = state.get("worker_configs", {}).get(WORKER_TYPE, {})
log_event(session_id, "session_validated", WORKER_TYPE, "Session state validated")
log_debug(session_id, "SUCCESS", WORKER_TYPE, f"Configuration loaded: {list(worker_config.keys())}")

# Step 4: Log Configuration Complete
log_event(session_id, "worker_configured", WORKER_TYPE, "Worker configuration complete")
log_debug(session_id, "INFO", WORKER_TYPE, "Starting task execution")

# Step 5: Begin Analysis
log_event(session_id, "worker_analysis_started", WORKER_TYPE, "Beginning domain analysis")
log_debug(session_id, "INFO", WORKER_TYPE, f"Complexity level: {worker_config.get('complexity_level', 'unknown')}")
```

## ✅ Mandatory Worker Completion Sequence

```python
# Step 1: Save Notes
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/{WORKER_TYPE.replace('-worker','')}-notes.md"
Write(notes_path, detailed_notes)
log_event(session_id, "worker_notes_created", WORKER_TYPE, f"Notes saved to {notes_path}")
log_debug(session_id, "SUCCESS", WORKER_TYPE, "Notes file created")

# Step 2: Save JSON Response
json_response = {
    "worker": WORKER_TYPE,
    "status": "completed",
    "summary": {...},
    "findings": [...],
    "recommendations": [...]
}
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/{WORKER_TYPE.replace('-worker','')}-response.json"
Write(json_path, json.dumps(json_response, indent=2))
log_event(session_id, "worker_json_provided", WORKER_TYPE, "JSON response saved")
log_debug(session_id, "SUCCESS", WORKER_TYPE, "JSON response persisted")

# Step 3: Log Completion
log_event(session_id, "worker_completed", WORKER_TYPE, f"Analysis complete - {len(findings)} findings")
log_debug(session_id, "SUCCESS", WORKER_TYPE, f"Worker completed successfully")
```

## 📝 Event Types Reference

### Mandatory Lifecycle Events (ALL WORKERS)
- `worker_spawned` - Worker activated
- `session_validated` - Session state verified
- `worker_configured` - Configuration loaded
- `worker_analysis_started` - Analysis begun
- `worker_notes_created` - Notes file written
- `worker_json_provided` - JSON response saved
- `worker_completed` - Task finished

### Debug Levels
- `INFO` - General information
- `SUCCESS` - Successful operations
- `WARNING` - Non-critical issues
- `ERROR` - Critical errors
- `COMPLIANCE` - Protocol compliance status

## 🔒 Implementation Rules

### For Worker Agents
```markdown
## Mandatory Startup Protocol

Execute the exact sequence from `.claude/protocols/unified-logging-protocol.md`:
1. Extract session ID using `extract_session_id()`
2. Log spawn event using `log_event()`
3. Validate session and log using both functions
4. Log configuration complete
5. Begin analysis with proper logging

Reference the protocol file for the exact functions - do not reimplement.
```

### For Queen Orchestrator
```python
# Verify worker compliance
def verify_worker_compliance(session_id, worker_name):
    """Check if worker properly logged lifecycle events"""
    events = Read(f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl")
    
    required_events = [
        "worker_spawned",
        "session_validated", 
        "worker_configured",
        "worker_analysis_started",
        "worker_completed"
    ]
    
    worker_events = []
    for line in events.strip().split('\n'):
        try:
            event = json.loads(line)
            if event.get("agent") == worker_name:
                worker_events.append(event.get("type"))
        except:
            continue
    
    missing = [e for e in required_events if e not in worker_events]
    
    if missing:
        log_debug(session_id, "WARNING", "queen-orchestrator", 
                 f"Worker {worker_name} missing events: {missing}")
    
    return len(missing) == 0
```

## ⚠️ ENFORCEMENT

1. **No Custom Implementations** - Workers MUST NOT create their own logging functions
2. **Reference This File** - All agents must reference this protocol
3. **Exact Function Names** - Use `log_event()` and `log_debug()` exactly as shown
4. **Complete Lifecycle** - All 7 mandatory events must be logged
5. **Atomic Operations** - Always use Bash echo for thread safety

## 🎯 Protocol Compliance Check

```python
# Quick compliance check for any agent
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
```

---

**This protocol is THE authoritative standard for all logging implementations.**