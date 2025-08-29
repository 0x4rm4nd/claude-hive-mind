# Worker Startup Protocol

#worker-startup #mandatory #session-initialization

## Purpose

Standardized startup sequence for all worker agents. This protocol ensures consistent session initialization, state verification, and coordination setup.

## Mandatory Startup Sequence

### Step 1: Session Extraction
```python
# Extract session ID from prompt
import re
WORKER_TYPE = "[worker-type]"  # e.g., "backend-worker"

if "Session ID:" in prompt:
    session_match = re.search(r"Session ID:\s*([^\s\n-]+)", prompt)
    session_id = session_match.group(1).strip() if session_match else None
else:
    # Generate from task description if not provided
    task_slug = re.sub(r'[^a-zA-Z0-9]+', '-', prompt[:100].lower())[:50]
    timestamp = Bash("date +'%Y-%m-%d-%H-%M'").strip()
    session_id = f"{timestamp}-{task_slug}"
```

### Step 2: Session Validation
```python
# Verify session directory exists
session_path = f"Docs/hive-mind/sessions/{session_id}"
if not exists(f"{session_path}/STATE.json"):
    raise Exception(f"FATAL: Session {session_id} not found")

# Read session state
state = json.loads(Read(f"{session_path}/STATE.json"))
worker_config = state["worker_configs"].get(WORKER_TYPE, {})
```

### Step 3: Log Worker Spawn
```python
# Log worker activation
log_event(session_id, "worker_spawned", WORKER_TYPE, "Worker activated")
log_debug(session_id, "INFO", WORKER_TYPE, "Starting task execution")
```

### Step 4: Execute Task
```python
# Perform assigned work based on worker specialization
# Use protocols from .claude/protocols/ for coordination
# Save outputs to standardized locations
```

### Step 5: Save Outputs
```python
# Save detailed notes
Write(f"{session_path}/workers/{worker_role}-notes.md", detailed_analysis)

# Save JSON response
json_response = {
    "worker": WORKER_TYPE,
    "status": "completed",
    "summary": {...},
    "findings": [...],
    "recommendations": [...]
}
Write(f"{session_path}/workers/json/{worker_role}-response.json", json_response)

# Log completion
log_event(session_id, "worker_completed", WORKER_TYPE, "Task complete")
```

## Output Standards

### JSON Response Structure
```json
{
  "worker": "worker-type",
  "status": "completed",
  "summary": {
    "overall_assessment": "string",
    "critical_issues": 0,
    "recommendations_count": 0
  },
  "findings": [
    {
      "category": "string",
      "severity": "critical|high|medium|low",
      "description": "string",
      "evidence": "string"
    }
  ],
  "recommendations": [
    {
      "priority": "immediate|short_term|long_term",
      "action": "string",
      "rationale": "string"
    }
  ]
}
```

### Notes File Structure
```markdown
# [Worker Type] Analysis
**Session**: [session-id]
**Date**: [timestamp]

## Executive Summary
[Brief overview]

## Detailed Findings
[Comprehensive analysis]

## Recommendations
[Actionable items]

## Evidence
[Supporting data]
```

## Coordination Events

Workers must log these events for coordination:

```python
# When blocked
log_event(session_id, "worker_blocking", WORKER_TYPE, {
    "blocked_on": "dependency",
    "target": "other-worker",
    "priority": "high"
})

# When unblocked
log_event(session_id, "worker_ready", WORKER_TYPE, {
    "unblocked": "dependency",
    "available": ["resource1", "resource2"]
})

# For decisions
log_event(session_id, "decision", WORKER_TYPE, {
    "decision": "technical choice",
    "rationale": "reasoning"
})
```

## Error Handling

```python
try:
    # Main execution
    perform_task()
except Exception as e:
    log_event(session_id, "worker_error", WORKER_TYPE, str(e))
    # Save partial results if possible
    Write(f"{session_path}/workers/{worker_role}-error.md", error_details)
    raise
```