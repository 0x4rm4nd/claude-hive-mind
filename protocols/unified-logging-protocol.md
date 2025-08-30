# 🔐 Unified Logging Protocol - Single Source of Truth

## Purpose
**THE AUTHORITATIVE LOGGING STANDARD** - All agents MUST use these exact functions for EVENTS.jsonl and DEBUG.jsonl logging. This protocol supersedes all other logging implementations.

## ⚠️ CRITICAL REQUIREMENTS
1. **NO INLINE IMPLEMENTATIONS** - Agents must NOT implement their own logging
2. **REFERENCE ONLY** - Agents must reference this protocol file
3. **EXACT FUNCTION USAGE** - Use the exact function signatures below
4. **MANDATORY LOGGING** - All lifecycle events MUST be logged

## 📋 Universal Session Extraction (Step 1 for ALL Agents)

**Function Template**: `.claude/protocols/templates/logging-functions.py`

### Function: `extract_session_id(prompt_text, worker_type)`
- **Purpose**: Universal session extraction - MUST be first operation
- **Returns**: Validated session ID from prompt or generates fallback
- **Validates**: Session directory and STATE.json existence
- **Raises**: Exception if session not found or invalid

## 🎯 EVENTS.jsonl Logging Function (Universal)

**Function Template**: `.claude/protocols/templates/logging-functions.py`

### Function: `log_event(session_id, event_type, agent_name, details, status=None)`
- **Purpose**: ATOMIC APPEND to EVENTS.jsonl - Thread-safe implementation
- **Parameters**:
  - `session_id`: Active session identifier (used for file path only, NOT included in event)
  - `event_type`: Type of event (see Event Types Reference) - standardized field name
  - `agent_name`: Name of the agent logging the event
  - `details`: Event details (max 500 chars)
  - `status`: Optional status field
- **Returns**: True on successful logging
- **Implementation**: Uses Bash echo for atomic append operations
- **CRITICAL**: session_id is ONLY used to determine file path, never included in the event object

## 🐛 DEBUG.jsonl Logging Function (Universal)

**Function Template**: `.claude/protocols/templates/logging-functions.py`

### Function: `log_debug(session_id, level, agent_name, message, context=None)`
- **Purpose**: ATOMIC APPEND to DEBUG.jsonl - Thread-safe implementation
- **Parameters**:
  - `session_id`: Active session identifier
  - `level`: INFO, SUCCESS, WARNING, ERROR, DECISION, or COMPLIANCE
  - `agent_name`: Name of the agent logging
  - `message`: Debug message (max 1000 chars)
  - `context`: Optional additional context data
- **Returns**: True on successful logging
- **Implementation**: Uses Bash echo for atomic append operations

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
log_event(session_id, "analysis_started", WORKER_TYPE, "Beginning domain analysis")
log_debug(session_id, "INFO", WORKER_TYPE, f"Complexity level: {worker_config.get('complexity_level', 'unknown')}")
```

## ✅ Mandatory Worker Completion Sequence

```python
# Step 1: Save Notes (Research Phase)
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/{WORKER_TYPE.replace('-worker','')}_notes.md"
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
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/{WORKER_TYPE.replace('-worker','')}_response.json"
Write(json_path, json.dumps(json_response, indent=2))
log_event(session_id, "worker_json_provided", WORKER_TYPE, "JSON response saved")
log_debug(session_id, "SUCCESS", WORKER_TYPE, "JSON response persisted")

# Step 3: Log Completion
log_event(session_id, "worker_completed", WORKER_TYPE, f"Analysis complete - {len(findings)} findings")
log_debug(session_id, "SUCCESS", WORKER_TYPE, f"Worker completed successfully")
```

## 📝 Event Types Reference

### Mandatory Lifecycle Events (ALL WORKERS)
- `worker_spawned` - Worker activated and joined session (FIRST EVENT - REQUIRED)
- `worker_configured` - Configuration loaded and validated
- `analysis_started` - Analysis/task execution begun (no worker prefix)
- `worker_progress` - Intermediate progress update (optional)
- `worker_completed` - Task finished successfully
- `worker_failed` - Task failed with error

### Queen-Specific Events
- `queen_spawned` - Queen orchestrator activated (NOT queen_reactivated_for_synthesis)
- `session_created` - Session structure initialized
- `workers_planned` - Worker selection completed
- `tasks_assigned` - All worker tasks assigned (single consolidated event)
- `workers_deployed` - Worker prompts created
- `synthesis_started` - Beginning result synthesis
- `synthesis_completed` - Final synthesis complete

### Coordination Events
- `handoff_requested` - Worker needs input from another
- `handoff_accepted` - Worker accepted handoff
- `blocker_reported` - Worker blocked on dependency
- `blocker_resolved` - Blocking issue resolved
- `escalation_required` - Queen intervention needed

### Debug Levels
- `INFO` - General information
- `SUCCESS` - Successful operations
- `WARNING` - Non-critical issues
- `ERROR` - Critical errors
- `DECISION` - Decision points and reasoning
- `COMPLIANCE` - Protocol compliance status

### Mandatory DEBUG Logging Points

1. **Startup Phase** (ALL workers MUST log):
   - Session ID extraction result
   - Protocol loading status
   - Configuration validation
   - Tool availability check

2. **Decision Points** (DECISION level):
   - Task decomposition reasoning
   - Research strategy selection
   - Implementation approach chosen
   - Error recovery decisions

3. **Operations** (INFO/SUCCESS level):
   - File operations (read/write)
   - External tool calls
   - Search/analysis operations
   - Coordination events

4. **Completion** (SUCCESS level):
   - Output validation results
   - Token usage summary
   - Performance metrics
   - Quality gate checks

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

**Function Template**: `.claude/protocols/templates/logging-functions.py`

### Function: `verify_worker_compliance(session_id, worker_name)`
- **Purpose**: Check if worker properly logged lifecycle events
- **Parameters**:
  - `session_id`: Active session identifier
  - `worker_name`: Name of worker to verify
- **Returns**: True if all required events present, False otherwise
- **Logs**: WARNING to DEBUG.jsonl if events missing

## ⚠️ ENFORCEMENT

1. **No Custom Implementations** - Workers MUST NOT create their own logging functions
2. **Reference This File** - All agents must reference this protocol
3. **Exact Function Names** - Use `log_event()` and `log_debug()` exactly as shown
4. **Complete Lifecycle** - All 7 mandatory events must be logged
5. **Atomic Operations** - Always use Bash echo for thread safety

## 🎯 Protocol Compliance Check

**Function Template**: `.claude/protocols/templates/logging-functions.py`

### Function: `check_my_compliance(session_id, worker_type)`
- **Purpose**: Self-check for protocol compliance
- **Parameters**:
  - `session_id`: Active session identifier
  - `worker_type`: Type of worker performing check
- **Returns**: True if at least 5 events logged, False otherwise
- **Output**: Prints compliance status to console

---

**This protocol is THE authoritative standard for all logging implementations.**