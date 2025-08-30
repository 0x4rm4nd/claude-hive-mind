# 🔧 Worker Enforcement Validation Protocol

## Overview
This protocol validates that workers are following the mandatory enforcement protocols, particularly TodoWrite usage and startup protocol compliance.

## Validation Checkpoints

### 1. Initial Startup Validation
**When:** Immediately after worker delegation
**What to check:**
- Worker response contains: "✅ Agent file .claude/agents/{worker-name}.md read and protocols loaded"
- Worker response contains: "✅ TodoWrite task tracking initialized"  
- Worker response contains: "✅ Mandatory startup protocol Steps 1-6 completed"

**Failure response:** If any missing, Queen must escalate with priority "critical"

### 2. Progress Tracking Validation
**When:** Every 15-20 minutes during active work
**What to check:**
- TodoWrite tool calls in worker session logs
- Progressive status updates in todo lists (pending → in_progress → completed)
- Worker notes files contain progress updates

**Validation commands:**
```bash
# Check for TodoWrite usage in session
grep -r "TodoWrite" "Docs/hive-mind/sessions/{session-id}/workers/"

# Verify progressive updates
grep -r "status.*completed" "Docs/hive-mind/sessions/{session-id}/"

# Check worker note updates
ls -la "Docs/hive-mind/sessions/{session-id}/workers/"
```

### 3. Completion Validation
**When:** Worker reports task completion
**What to check:**
- Final TodoWrite update with all tasks marked "completed"
- Archive/reflect workflow execution
- Worker notes contain comprehensive findings

## Automated Validation Tools

### Queen Validation Commands
```python
def validate_worker_compliance(session_id, worker_name):
    """Validate worker followed enforcement protocols"""
    checks = []
    
    # Check 1: TodoWrite initialization
    worker_notes = f"Docs/hive-mind/sessions/{session_id}/workers/{worker_name}-notes.md"
    if "TodoWrite task list created" in read_file(worker_notes):
        checks.append("✅ TodoWrite initialization confirmed")
    else:
        checks.append("❌ TodoWrite initialization MISSING")
    
    # Check 2: Progress tracking
    if "TodoWrite list updated with current progress" in read_file(worker_notes):
        checks.append("✅ Progress tracking active")
    else:
        checks.append("❌ Progress tracking MISSING")
    
    # Check 3: Startup protocol
    if "✅ Agent file .claude/agents/" in read_file(worker_notes):
        checks.append("✅ Startup protocol confirmed")
    else:
        checks.append("❌ Startup protocol MISSING")
    
    return checks

def escalate_compliance_failure(worker_name, missing_elements):
    """Escalate when worker fails compliance"""
    event = {
        "type": "escalation",
        "priority": "critical",
        "worker": worker_name,
        "violation": "enforcement_protocol_failure",
        "missing": missing_elements,
        "action_required": "immediate_correction"
    }
    log_escalation_event(event)
```

### Session Audit Commands
```python
def audit_session_compliance(session_id):
    """Audit entire session for protocol compliance"""
    session_dir = f"Docs/hive-mind/sessions/{session_id}"
    workers = get_active_workers(session_dir)
    
    compliance_report = {
        "session_id": session_id,
        "total_workers": len(workers),
        "compliant_workers": 0,
        "violations": []
    }
    
    for worker in workers:
        validation = validate_worker_compliance(session_id, worker)
        violations = [v for v in validation if "❌" in v]
        
        if not violations:
            compliance_report["compliant_workers"] += 1
        else:
            compliance_report["violations"].append({
                "worker": worker,
                "violations": violations
            })
    
    # Calculate compliance rate
    compliance_rate = (compliance_report["compliant_workers"] / compliance_report["total_workers"]) * 100
    compliance_report["compliance_rate"] = compliance_rate
    
    return compliance_report
```

## Enforcement Actions

### Non-Compliance Response
1. **First Violation**: Warning escalation with 5-minute correction window
2. **Second Violation**: Critical escalation with immediate Queen intervention
3. **Third Violation**: Worker replaced with compliant backup

### Compliance Incentives
- Compliant workers get priority for complex task assignments
- Compliance metrics tracked for worker performance evaluation
- High-compliance sessions get archived as exemplary patterns

## Integration with Existing Protocols

### Session Coordination
- Add compliance validation to session STATE.json
- Track enforcement metrics in session EVENTS.jsonl
- Include compliance report in session completion

### Task Management
- Link TodoWrite compliance to Archon task status
- Require compliance validation before task completion
- Archive compliance patterns for future sessions

## Success Metrics

### Target Compliance Rates
- **TodoWrite Usage**: 100% (no exceptions)
- **Startup Protocol**: 100% (no exceptions) 
- **Progress Tracking**: 95% (allow minor delays)
- **Archive/Reflect**: 90% (complexity-dependent)

### Monitoring Dashboard
Track these metrics across all sessions:
- Compliance rate per worker type
- Most common violations
- Time to correction after violation
- Impact of compliance on session success

This validation protocol ensures the enforcement systems actually work and aren't just ignored by workers.