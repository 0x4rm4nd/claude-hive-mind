# Worker Startup Protocol

#worker-startup #mandatory #session-initialization #output-enforcement

## Purpose

Standardized startup sequence for all worker agents with MANDATORY output file generation. This protocol ensures consistent session initialization, state verification, coordination setup, and output validation.

## 🚨 CRITICAL: Mandatory Output Requirements

**ALL WORKERS MUST GENERATE TWO OUTPUT FILES:**
1. **Analysis Markdown**: `workers/decisions/{worker-name}-analysis.md`
2. **Structured JSON**: `workers/json/{worker-name}.json`

**Failure to generate both files is a PROTOCOL VIOLATION that blocks session completion.**

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

### Step 5: Save Outputs (MANDATORY)
```python
# MANDATORY: Save detailed analysis markdown
# Path: workers/decisions/{worker-name}-analysis.md
analysis_content = generate_detailed_analysis()  # Worker-specific analysis
Write(f"{session_path}/workers/decisions/{WORKER_TYPE}-analysis.md", analysis_content)

# MANDATORY: Save structured JSON response
# Path: workers/json/{worker-name}.json
json_response = {
    "worker": WORKER_TYPE,
    "status": "completed",
    "timestamp": datetime.now().isoformat(),
    "session_id": session_id,
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
    ],
    "files_modified": [],
    "implementation_details": {}
}
Write(f"{session_path}/workers/json/{WORKER_TYPE}.json", json_response)

# MANDATORY: Validate outputs exist
if not exists(f"{session_path}/workers/decisions/{WORKER_TYPE}-analysis.md"):
    raise Exception(f"PROTOCOL VIOLATION: Missing analysis file for {WORKER_TYPE}")
if not exists(f"{session_path}/workers/json/{WORKER_TYPE}.json"):
    raise Exception(f"PROTOCOL VIOLATION: Missing JSON file for {WORKER_TYPE}")

# Log completion only after outputs validated
log_event(session_id, "worker_completed", WORKER_TYPE, {
    "status": "success",
    "outputs_generated": [
        f"workers/decisions/{WORKER_TYPE}-analysis.md",
        f"workers/json/{WORKER_TYPE}.json"
    ]
})
```

## Output Standards

### JSON Response Structure (MANDATORY)
**File Path**: `workers/json/{worker-name}.json`

```json
{
  "worker": "worker-type",
  "session_id": "session-id",
  "timestamp": "ISO-8601 timestamp",
  "status": "completed",
  "summary": {
    "overall_assessment": "string",
    "work_completed": "string",
    "critical_issues": 0,
    "recommendations_count": 0,
    "files_modified": 0
  },
  "findings": [
    {
      "id": "finding-001",
      "category": "security|performance|quality|architecture|implementation",
      "severity": "critical|high|medium|low",
      "title": "string",
      "description": "string",
      "evidence": "string",
      "location": "file:line or component"
    }
  ],
  "recommendations": [
    {
      "id": "rec-001",
      "priority": "immediate|short_term|long_term",
      "category": "string",
      "action": "string",
      "rationale": "string",
      "effort": "low|medium|high",
      "impact": "low|medium|high"
    }
  ],
  "implementation": {
    "files_modified": [],
    "files_created": [],
    "files_deleted": [],
    "tests_added": [],
    "dependencies_added": [],
    "configuration_changes": []
  },
  "metrics": {
    "execution_time_seconds": 0,
    "tokens_used": 0,
    "files_analyzed": 0,
    "lines_modified": 0
  },
  "dependencies": {
    "blocked_by": [],
    "blocking": [],
    "coordinated_with": []
  }
}
```

### Analysis Markdown Structure (MANDATORY)
**File Path**: `workers/decisions/{worker-name}-analysis.md`

```markdown
# [Worker Type] Analysis Report
**Session**: [session-id]
**Generated**: [ISO-8601 timestamp]
**Worker**: [worker-name]

## Executive Summary
[High-level overview of work completed, findings, or analysis]

## Detailed Analysis
### Primary Focus Area
[Detailed examination of main task area]

### Secondary Considerations
[Additional findings or observations]

### Technical Details
[Implementation specifics, code changes, or technical decisions]

## Findings
### Critical Issues
[Any critical problems identified]

### Improvements Needed
[Areas requiring attention]

### Positive Observations
[What's working well]

## Recommendations
### Immediate Actions
[Things that need immediate attention]

### Short-term Improvements
[Changes to implement soon]

### Long-term Considerations
[Strategic improvements]

## Evidence & References
[Supporting data, code snippets, or references]

## Files Modified
[List of files changed during this worker's execution]

## Metrics
- Lines analyzed: [number]
- Issues found: [number]
- Recommendations made: [number]
- Files modified: [number]
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

## Output Validation & Enforcement

### Validation Checklist
```python
# Every worker MUST validate outputs before completion
def validate_worker_outputs(session_path, worker_type):
    """Validate mandatory output files exist and are non-empty"""
    violations = []
    
    # Check analysis markdown
    analysis_path = f"{session_path}/workers/decisions/{worker_type}-analysis.md"
    if not exists(analysis_path):
        violations.append(f"Missing analysis file: {analysis_path}")
    elif file_size(analysis_path) < 100:  # Minimum 100 bytes
        violations.append(f"Analysis file too small: {analysis_path}")
    
    # Check JSON output
    json_path = f"{session_path}/workers/json/{worker_type}.json"
    if not exists(json_path):
        violations.append(f"Missing JSON file: {json_path}")
    else:
        try:
            data = json.loads(Read(json_path))
            # Validate required fields
            required = ['worker', 'session_id', 'status', 'summary', 'findings']
            for field in required:
                if field not in data:
                    violations.append(f"JSON missing required field: {field}")
        except:
            violations.append(f"Invalid JSON format: {json_path}")
    
    if violations:
        raise Exception(f"OUTPUT VALIDATION FAILED:\n" + "\n".join(violations))
    
    return True
```

### Protocol Compliance Verification
```python
# Queen orchestrator verifies all workers generated outputs
def verify_worker_compliance(session_path, workers_list):
    """Verify all workers followed output protocol"""
    compliance_report = {
        "compliant": [],
        "violations": {}
    }
    
    for worker in workers_list:
        try:
            validate_worker_outputs(session_path, worker)
            compliance_report["compliant"].append(worker)
        except Exception as e:
            compliance_report["violations"][worker] = str(e)
    
    # Log compliance report
    log_event(session_id, "protocol_compliance_check", "queen-orchestrator", compliance_report)
    
    if compliance_report["violations"]:
        # Protocol violation detected - require correction
        raise Exception(f"PROTOCOL VIOLATIONS DETECTED: {compliance_report['violations']}")
    
    return compliance_report
```

## Error Handling

```python
try:
    # Main execution
    perform_task()
    
    # MANDATORY: Generate outputs
    save_analysis(detailed_analysis)
    save_json(structured_data)
    
    # MANDATORY: Validate outputs
    validate_worker_outputs(session_path, WORKER_TYPE)
    
except Exception as e:
    log_event(session_id, "worker_error", WORKER_TYPE, {
        "error": str(e),
        "type": "protocol_violation" if "PROTOCOL" in str(e) else "execution_error"
    })
    
    # Still try to save partial results
    try:
        Write(f"{session_path}/workers/decisions/{WORKER_TYPE}-error.md", f"""
# Error Report: {WORKER_TYPE}
## Session: {session_id}
## Error: {str(e)}
## Partial Results:
{partial_results if exists else "No partial results available"}
""")
    except:
        pass  # Best effort
    
    raise
```

## Enforcement & Consequences

### Protocol Violations
1. **Missing Analysis File**: Session cannot complete, worker marked as failed
2. **Missing JSON File**: Session cannot complete, worker marked as failed
3. **Invalid JSON Structure**: Worker must regenerate with correct structure
4. **Incomplete Fields**: Worker must complete all required fields

### Queen Orchestrator Enforcement
- Queen checks for output files before marking workers complete
- Missing outputs trigger worker re-execution or escalation
- Session synthesis blocked until all workers have valid outputs
- Protocol violations logged and tracked for system improvement