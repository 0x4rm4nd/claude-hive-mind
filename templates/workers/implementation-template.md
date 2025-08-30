# Worker Implementation Template - Event Logging Standards

## 🚨 CRITICAL: Mandatory Worker Startup Sequence

### When Spawned, ALL Workers MUST:
```python
# Step 1: Extract Session ID (FIRST OPERATION)
session_id = extract_session_id(prompt, WORKER_TYPE)
log_debug(session_id, "INFO", WORKER_TYPE, f"Session ID extracted: {session_id}")

# Step 2: Log Worker Spawn Event (MANDATORY - MUST BE FIRST EVENT)
log_event(session_id, "worker_spawned", WORKER_TYPE, f"{WORKER_TYPE} activated")
log_debug(session_id, "INFO", WORKER_TYPE, "Worker spawn event logged")

# Step 3: Validate Session State
state = json.loads(Read(f"Docs/hive-mind/sessions/{session_id}/STATE.json"))
worker_config = state.get("worker_configs", {}).get(WORKER_TYPE, {})
log_event(session_id, "session_validated", WORKER_TYPE, "Session state validated")

# Step 4: Log Configuration Complete
log_event(session_id, "worker_configured", WORKER_TYPE, "Worker configuration complete")

# Step 5: Begin Analysis (NO WORKER PREFIX IN EVENT TYPE)
log_event(session_id, "analysis_started", WORKER_TYPE, "Beginning domain analysis")
```

## 📝 CRITICAL: Event Logging Standards

### Event Structure (NO session_id in event object)
```json
{
  "timestamp": "2025-08-30T14:16:22Z",
  "type": "analysis_started",  // NO worker-specific prefixes
  "agent": "backend-worker",
  "details": {
    "action": "analysis_initialized",  // NO worker prefix here either
    "target": "crypto-data",
    "result": "success"
  }
}
```

### ❌ INCORRECT Event Examples (DO NOT USE)
```json
// WRONG - includes session_id in event
{
  "timestamp": "2025-08-30T14:16:22Z",
  "type": "task_started",
  "agent": "backend-worker",
  "session_id": "2025-08-30-session",  // NEVER include this!
  "details": {...}
}

// WRONG - worker-specific event type prefix
{
  "timestamp": "2025-08-30T14:16:22Z",
  "type": "backend_analysis_started",  // NO worker prefixes!
  "agent": "backend-worker",
  "details": {...}
}

// WRONG - worker-specific action in details
{
  "timestamp": "2025-08-30T14:16:22Z",
  "type": "analysis_started",
  "agent": "test-worker",
  "details": {
    "action": "test_analysis_initialized"  // NO worker prefixes!
  }
}
```

### ✅ CORRECT Event Examples
```json
// CORRECT - worker_spawned (first event)
{
  "timestamp": "2025-08-30T14:16:22Z",
  "type": "worker_spawned",
  "agent": "backend-worker",
  "details": "backend-worker activated"
}

// CORRECT - analysis_started (no prefix)
{
  "timestamp": "2025-08-30T14:16:22Z",
  "type": "analysis_started",
  "agent": "backend-worker",
  "details": {
    "action": "analysis_initialized",
    "target": "crypto-data",
    "result": "success"
  }
}
```

## 📄 CRITICAL: Output File Requirements

### MANDATORY: Create TWO Output Files

#### 1. Research Notes (Markdown)
```python
# CORRECT file naming (underscore, no "-worker")
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/backend_notes.md"
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/test_notes.md"

# WRONG (do not use)
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/backend-worker-notes.md"
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/backend-notes.md"
```

#### 2. JSON Response
```python
# CORRECT file naming
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/backend_response.json"
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/test_response.json"

# Helper for clean worker type
worker_type_clean = WORKER_TYPE.replace('-worker', '')
```

### Output Creation Sequence
```python
# Step 1: Create markdown notes FIRST
notes_content = generate_markdown_report(findings)
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/{WORKER_TYPE.replace('-worker','')}_notes.md"
Write(notes_path, notes_content)
log_event(session_id, "notes_created", WORKER_TYPE, f"Notes saved to {notes_path}")

# Step 2: Create JSON response SECOND  
json_response = generate_json_response(findings)
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/{WORKER_TYPE.replace('-worker','')}_response.json"
Write(json_path, json.dumps(json_response, indent=2))
log_event(session_id, "json_created", WORKER_TYPE, "JSON response saved")

# Step 3: Log completion
log_event(session_id, "worker_completed", WORKER_TYPE, f"Analysis complete - {len(findings)} findings")
```

## 🔒 Compliance Checklist

Before completing work, verify:
- [ ] `worker_spawned` event logged as FIRST event
- [ ] NO `session_id` field in any event objects
- [ ] NO worker-specific prefixes in event types
- [ ] Both output files created (markdown AND JSON)
- [ ] Files use correct naming (underscore, no "-worker")
- [ ] Files in correct directories (workers/ and workers/json/)
- [ ] All mandatory lifecycle events logged

## 📋 Event Type Reference

### Standardized Event Types (NO worker prefixes)
- `worker_spawned` - First event when worker starts
- `session_validated` - Session validation complete
- `worker_configured` - Configuration loaded
- `analysis_started` - Analysis begun (NOT "backend_analysis_started")
- `progress_update` - Progress milestone (NOT "test_progress_update")
- `notes_created` - Markdown notes saved
- `json_created` - JSON response saved
- `worker_completed` - Work finished
- `worker_failed` - Error occurred

### Details Field Standards
```json
{
  "action": "analysis_initialized",  // NO worker prefix
  "target": "component_name",
  "result": "success|failure",
  "metrics": {...}  // Optional
}
```

---

**This template defines the MANDATORY standards for all worker implementations.**
