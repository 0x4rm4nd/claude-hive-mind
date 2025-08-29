# Critical Session Management Instructions

## MANDATORY SESSION PATH CONSISTENCY

### Path Detection Requirements
**CRITICAL**: All workers MUST use the unified session management system to ensure path consistency.

1. **Project Root Detection**:
   - NEVER use relative paths from your current working directory
   - ALWAYS use `SessionManagement.detect_project_root()` from `.claude/protocols/session_management.py`
   - Session path MUST be: `{project_root}/Docs/hive-mind/sessions/{session_id}`
   - NEVER create sessions in subdirectories like `crypto-data/Docs/hive-mind/sessions/`

2. **Session Path Validation**:
   - Before ANY file operation, validate you're using the correct session path
   - Use `SessionManagement.get_session_path(session_id)` for all path operations
   - If path mismatch detected, STOP and report error immediately

### File Operation Requirements

**CRITICAL**: NEVER overwrite existing session files. ALL operations must be append-only or atomic updates.

1. **EVENTS.jsonl Operations**:
   - ALWAYS use `SessionManagement.append_to_events(session_id, event_data)`
   - NEVER use Write() or direct file operations on EVENTS.jsonl
   - NEVER overwrite or recreate EVENTS.jsonl after initial creation
   - Each event MUST be a single line of JSON followed by newline

2. **DEBUG.jsonl Operations**:
   - ALWAYS use `SessionManagement.append_to_debug(session_id, debug_data)`
   - NEVER use Write() or direct file operations on DEBUG.jsonl
   - NEVER overwrite or recreate DEBUG.jsonl after initial creation
   - Each debug entry MUST be a single line of JSON followed by newline

3. **STATE.json Operations**:
   - ALWAYS use `SessionManagement.update_state_atomically(session_id, updates)`
   - This method reads existing state, merges updates, and writes back atomically
   - NEVER use Write() to overwrite STATE.json completely
   - ALWAYS preserve existing data when updating STATE.json

4. **BACKLOG.jsonl Operations**:
   - ALWAYS use `SessionManagement.append_to_backlog(session_id, item)`
   - NEVER overwrite or recreate BACKLOG.jsonl
   - Each backlog item MUST be a single line of JSON followed by newline

### Worker File Creation

When creating worker-specific files:
- Use `SessionManagement.create_worker_file(session_id, worker_type, file_type, content)`
- Valid file_types: 'json', 'prompt', 'decision'
- Files are created in correct subdirectories automatically

### Session Validation

Before starting ANY work:
1. Validate session exists: `SessionManagement.ensure_session_exists(session_id)`
2. Read current state: `SessionManagement.read_state(session_id)`
3. Log worker activity: `SessionManagement.log_worker_activity(session_id, worker_type, activity)`

### Error Handling

If ANY of these conditions occur, STOP immediately:
- Cannot find project root
- Session path doesn't match expected location
- File append operations fail
- State update fails

Report the error to EVENTS.jsonl and notify Queen immediately.

## Implementation Example

```python
from .protocols.session_management import SessionManagement

# At worker startup
session_id = extract_session_id()  # From prompt or context
if not SessionManagement.ensure_session_exists(session_id):
    raise ValueError(f"Session {session_id} not found or invalid")

# Log worker startup
SessionManagement.append_to_events(session_id, {
    "type": "worker_spawned",
    "agent": "your-worker-type",
    "status": "initializing"
})

# Read configuration
state = SessionManagement.read_state(session_id)
worker_config = state.get("worker_configs", {}).get("your-worker-type", {})

# During work - log activity
SessionManagement.log_worker_activity(
    session_id, 
    "your-worker-type",
    "Analyzing component X",
    {"component": "X", "progress": 0.5}
)

# Update state atomically
SessionManagement.update_state_atomically(session_id, {
    "coordination_status": {
        "your-worker-type": {
            "status": "in_progress",
            "progress": 0.5
        }
    }
})

# On completion
SessionManagement.create_worker_file(
    session_id,
    "your-worker-type",
    "json",
    results_dict
)
```

## Compliance Verification

Each worker MUST verify compliance with these requirements:
1. ✓ Using unified path detection
2. ✓ Never overwriting session files
3. ✓ Using append methods for logs
4. ✓ Using atomic update for STATE.json
5. ✓ Validating session before work
6. ✓ Logging all activities to EVENTS.jsonl

Failure to comply will result in coordination failures and data loss.