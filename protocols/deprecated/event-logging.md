# Event Logging Protocol - Session Activity Tracking

## 🎯 MANDATORY EVENT LOGGING FOR ALL AGENTS

**All agents MUST log critical events to EVENTS.jsonl for session tracking and resumption capability.**

### 📝 **Event Logging Function**

```python
def log_session_event(session_id, event_type, agent_name, details, status=None):
    """RACE-CONDITION-FREE event logging with atomic append operations"""
    import json
    from datetime import datetime
    import re
    
    try:
        # Generate accurate local timestamp with validation
        current_time = datetime.now()
        timestamp = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        
        # CRITICAL: Extract session timestamp to validate temporal consistency
        try:
            session_hour = int(session_id.split('-')[3])  # Extract hour from session ID
            current_hour = current_time.hour
            
            # Prevent impossible timestamps (more than 2 hours deviation)
            if abs(current_hour - session_hour) > 2:
                print(f"⚠️ Timestamp validation warning: session hour {session_hour}, current hour {current_hour}")
                # Use session-relative timestamp to maintain consistency
                corrected_time = current_time.replace(hour=session_hour, minute=current_time.minute)
                timestamp = corrected_time.strftime('%Y-%m-%dT%H:%M:%SZ')
                print(f"🔧 Corrected timestamp: {timestamp}")
        except:
            pass  # Continue with original timestamp if validation fails
        
        # Validate inputs
        if not session_id or not event_type or not agent_name:
            print(f"⚠️ Invalid event data: session_id={session_id}, type={event_type}, agent={agent_name}")
            return False
            
        # Sanitize details to prevent JSON corruption
        if isinstance(details, str):
            details = details.replace('"', "'").replace('\n', ' ').strip()
        
        # Build validated event
        event = {
            "timestamp": timestamp,
            "type": event_type,
            "agent": agent_name,
            "details": str(details)[:500]  # Prevent oversized events
        }
        
        if status:
            event["status"] = status
        
        # Validate JSON serialization
        try:
            json_string = json.dumps(event, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            print(f"⚠️ JSON serialization error: {e}")
            return False
            
        # CRITICAL FIX: Use Bash echo for atomic append (prevents race conditions)
        events_file = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
        
        try:
            # ATOMIC APPEND: Use bash echo to append single line atomically
            # This prevents race conditions when multiple workers log simultaneously
            import subprocess
            import os
            
            # Ensure session directory exists
            session_dir = f"Docs/hive-mind/sessions/{session_id}"
            try:
                Bash(command=f"mkdir -p '{session_dir}'", description="Ensure session directory exists")
            except:
                pass  # Directory might already exist
            
            # ATOMIC APPEND: Single bash operation prevents corruption
            escaped_json = json_string.replace("'", "'\"'\"'")  # Escape single quotes for bash
            append_command = f"echo '{escaped_json}' >> '{events_file}'"
            
            try:
                Bash(command=append_command, description=f"Atomic append event for {agent_name}")
                print(f"✅ Event logged atomically: {agent_name} - {event_type}")
                return True
            except Exception as e:
                print(f"⚠️ Atomic append failed, trying fallback: {e}")
                # Fallback to Write method if Bash fails
                return fallback_write_event(events_file, json_string)
                
        except Exception as e:
            print(f"⚠️ Event logging failed: {e}")
            return False
            
        return True
        
    except Exception as e:
        print(f"🚨 Critical event logging error: {e}")
        return False

def fallback_write_event(events_file, json_string):
    """Fallback Write-based event logging (less safe but available if Bash fails)"""
    try:
        # Try to read existing file
        try:
            current_content = Read(events_file)
            if current_content.strip():
                # File has content - ensure proper JSONL format
                if not current_content.endswith('\n'):
                    Write(events_file, current_content + '\n' + json_string + '\n')
                else:
                    Write(events_file, current_content + json_string + '\n')
            else:
                Write(events_file, json_string + '\n')
        except:
            # File doesn't exist - create with first event
            Write(events_file, json_string + '\n')
        return True
    except:
        return False
```

### 🚨 **MANDATORY EVENT TYPES**

#### **Session Lifecycle Events**
- `session_started` - Session initialization
- `session_completed` - Session finished successfully  
- `session_failed` - Session terminated with errors

#### **Queen Orchestrator Events**
- `queen_spawned` - Queen agent activated
- `coordination_started` - Queen begins coordination analysis
- `workers_planned` - Queen determines worker requirements
- `workers_spawn_initiated` - Queen triggers worker spawning
- `synthesis_started` - Queen begins result synthesis
- `synthesis_completed` - Queen completes final synthesis

#### **Worker Events**
- `worker_spawned` - Worker agent activated
- `worker_configured` - Worker loaded session configuration
- `worker_analysis_started` - Worker begins analysis tasks
- `worker_notes_created` - Worker completed detailed notes
- `worker_json_provided` - Worker provided coordination JSON
- `worker_completed` - Worker finished all tasks
- `worker_failed` - Worker encountered critical error

#### **File Operations Events**
- `file_created` - Important session file created
- `file_updated` - Session file modified
- `notes_written` - Worker notes file written
- `synthesis_document_created` - Research synthesis created

### 🔧 **AGENT-SPECIFIC LOGGING REQUIREMENTS**

#### **Queen Orchestrator Must Log:**
```python
# At start
log_session_event(session_id, "queen_spawned", "queen-orchestrator", "Coordination analysis initiated")

# During planning
log_session_event(session_id, "workers_planned", "queen-orchestrator", 
    f"Required workers: {worker_list}", status="analysis_complete")

# During worker spawning
log_session_event(session_id, "workers_spawn_initiated", "queen-orchestrator",
    f"Spawning {len(workers)} workers in parallel")

# During synthesis  
log_session_event(session_id, "synthesis_started", "queen-orchestrator", 
    "Reading worker detailed notes for comprehensive synthesis")

log_session_event(session_id, "synthesis_completed", "queen-orchestrator",
    f"Cross-domain synthesis complete with {len(findings)} key insights")
```

#### **All Workers Must Log:**
```python
# At startup
log_session_event(session_id, "worker_spawned", worker_type, "Worker agent activated")

# After configuration
log_session_event(session_id, "worker_configured", worker_type, "Session configuration loaded")

# When starting analysis  
log_session_event(session_id, "worker_analysis_started", worker_type, "Beginning domain analysis")

# After creating notes
log_session_event(session_id, "worker_notes_created", worker_type, 
    f"Detailed notes written to {notes_file_path}")

# After JSON response
log_session_event(session_id, "worker_json_provided", worker_type, "Coordination JSON provided to Queen")

# At completion
log_session_event(session_id, "worker_completed", worker_type, 
    f"Analysis complete - {analysis_duration} duration, {findings_count} findings")
```

### 📊 **EVENT LOG VALIDATION & REPAIR**

**Session Health Check:**
```python
def validate_and_heal_session_events(session_id):
    """Validate and automatically fix session event issues"""
    import json
    
    events_file = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
    
    try:
        # Read and validate each line
        raw_content = Read(events_file)
        if not raw_content:
            return {"valid": False, "error": "Empty events file", "events": []}
            
        valid_events = []
        corrupted_lines = []
        
        for line_num, line in enumerate(raw_content.strip().split('\n'), 1):
            if not line.strip():
                continue
                
            try:
                event = json.loads(line.strip())
                
                # Validate required fields
                if all(field in event for field in ["timestamp", "type", "agent", "details"]):
                    # Validate timestamp format
                    if re.match(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', event["timestamp"]):
                        valid_events.append(event)
                    else:
                        print(f"⚠️ Invalid timestamp on line {line_num}: {event['timestamp']}")
                        corrupted_lines.append((line_num, "invalid_timestamp"))
                else:
                    print(f"⚠️ Missing required fields on line {line_num}")
                    corrupted_lines.append((line_num, "missing_fields"))
                    
            except json.JSONDecodeError:
                print(f"⚠️ Invalid JSON on line {line_num}: {line[:50]}...")
                corrupted_lines.append((line_num, "invalid_json"))
                
        # Auto-heal if corrupted lines found
        if corrupted_lines:
            print(f"🔧 Healing {len(corrupted_lines)} corrupted lines...")
            healed_content = '\n'.join(json.dumps(event) for event in valid_events) + '\n'
            Write(events_file, healed_content)
            
        # Check for required events
        required_events = ["queen_spawned", "workers_planned", "synthesis_completed"]
        missing_events = []
        
        for event_type in required_events:
            if not any(e["type"] == event_type for e in valid_events):
                missing_events.append(event_type)
        
        return {
            "valid": len(missing_events) == 0 and len(corrupted_lines) == 0,
            "missing_events": missing_events,
            "corrupted_lines": len(corrupted_lines),
            "total_events": len(valid_events),
            "events": valid_events
        }
        
    except Exception as e:
        return {"valid": False, "error": str(e), "events": []}
```

### 🔄 **SESSION RESUMPTION CAPABILITY**

**Resume Session Function:**
```python
def resume_session_from_events(session_id):
    """Resume session state from event log"""
    events = read_events_jsonl(session_id)
    
    session_state = {
        "workers_completed": [],
        "files_created": [],
        "current_phase": "unknown",
        "last_activity": None
    }
    
    for event in events:
        if event["type"] == "worker_completed":
            session_state["workers_completed"].append(event["agent"])
        elif event["type"] == "file_created":
            session_state["files_created"].append(event["details"])
        elif event["type"] == "synthesis_completed":
            session_state["current_phase"] = "synthesis_complete"
            
        session_state["last_activity"] = event["timestamp"]
    
    return session_state
```

### 🧠 **EVENT DEDUPLICATION**

**Prevent duplicate events:**
```python
def log_event_with_deduplication(session_id, event_type, agent_name, details, status=None):
    """Log event with automatic deduplication"""
    # Read recent events to check for duplicates
    try:
        events_file = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
        recent_content = Read(events_file)
        
        if recent_content:
            lines = recent_content.strip().split('\n')[-10:]  # Check last 10 events
            for line in lines:
                try:
                    event = json.loads(line)
                    # Check for duplicate within last 5 minutes
                    if (event.get("type") == event_type and 
                        event.get("agent") == agent_name and
                        event.get("details") == str(details)[:100]):
                        print(f"📝 Skipping duplicate event: {event_type} from {agent_name}")
                        return True  # Skip duplicate
                except:
                    continue
                    
    except:
        pass  # Continue with logging if check fails
        
    return log_session_event(session_id, event_type, agent_name, details, status)
```

## 🚨 **ENFORCEMENT RULES**

1. **Every agent MUST use bulletproof logging function**
2. **Auto-healing prevents event log corruption** 
3. **Deduplication prevents spam events**
4. **Input validation prevents malformed entries**
5. **Graceful failure - logging errors don't crash agents**
6. **Session health monitoring with automatic fixes**
7. **Timestamp consistency across all agents**

This protocol ensures reliable session tracking with automatic error recovery.

## 🚨 **ESCALATION AND COORDINATION FUNCTIONS**

**Worker Coordination and Escalation Support:**

```python
import time
import json

def current_time():
    """Get current timestamp for timing operations"""
    return time.time()

def filter_events_after(timestamp_threshold, session_id):
    """Filter events that occurred after the given timestamp"""
    events_file = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
    try:
        content = Read(events_file)
        if not content.strip():
            return []
            
        filtered_events = []
        for line in content.strip().split('\n'):
            if line.strip():
                try:
                    event = json.loads(line)
                    # Convert timestamp to epoch for comparison
                    event_time = time.mktime(time.strptime(event["timestamp"], '%Y-%m-%dT%H:%M:%SZ'))
                    if event_time > timestamp_threshold:
                        filtered_events.append(event)
                except:
                    continue
        return filtered_events
    except:
        return []

def filter_events_where_type_is(session_id, event_type):
    """Filter events by type"""
    events_file = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
    try:
        content = Read(events_file)
        if not content.strip():
            return []
            
        filtered_events = []
        for line in content.strip().split('\n'):
            if line.strip():
                try:
                    event = json.loads(line)
                    if event.get("type") == event_type:
                        filtered_events.append(event)
                except:
                    continue
        return filtered_events
    except:
        return []

def log_escalation_event(session_id, current_agent, target_agent, reason="blocked"):
    """Log escalation event when worker needs help"""
    details = f"Escalating from {current_agent} to {target_agent} - reason: {reason}"
    return log_session_event(session_id, "escalation", current_agent, details)

def handle_critical_event(event, session_id, current_agent):
    """Handle critical priority events (2 minute response required)"""
    response_details = f"Responding to critical event: {event.get('details', 'unknown')}"
    log_session_event(session_id, "critical_response", current_agent, response_details)
    # Agents should implement specific critical event handling here

def handle_high_priority_event(event, session_id, current_agent):
    """Handle high priority events (5 minute response required)"""
    response_details = f"Responding to high priority event: {event.get('details', 'unknown')}"
    log_session_event(session_id, "high_priority_response", current_agent, response_details)
    # Agents should implement specific high priority event handling here

def handle_within_5_minutes(event, session_id, current_agent):
    """Handle medium priority events (5 minute response required)"""
    response_details = f"Responding to medium priority event: {event.get('details', 'unknown')}"
    log_session_event(session_id, "medium_priority_response", current_agent, response_details)
    # Agents should implement specific medium priority event handling here

def handle_within_10_minutes(event, session_id, current_agent):
    """Handle low priority events (10 minute response required)"""
    response_details = f"Responding to low priority event: {event.get('details', 'unknown')}"
    log_session_event(session_id, "low_priority_response", current_agent, response_details)
    # Agents should implement specific low priority event handling here
```

### 📋 **COORDINATION EVENT TYPES**

#### **Escalation Events**
- `escalation` - Worker escalating to another worker for help
- `critical_response` - Worker responding to critical priority event
- `high_priority_response` - Worker responding to high priority event
- `worker_blocked` - Worker blocked and waiting for dependencies
- `worker_unblocked` - Worker dependency resolved, resuming work

#### **Usage in Agent Files**
Workers should reference these functions as defined in event-logging protocol:

```python
# Import from event logging protocol
# Reference: .claude/protocols/event-logging.md

# Example usage in worker:
if blocked and (current_time() - blocked_start) > escalation_timeout:
    log_escalation_event(session_id, "backend-worker", "service-architect", "database design needed")
```