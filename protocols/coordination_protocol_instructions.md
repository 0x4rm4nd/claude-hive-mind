# Coordination Protocol Instructions

## Purpose
The Coordination Protocol manages multi-agent task coordination, session creation, event logging, and cross-worker communication for the SmartWalletFX hive-mind system.

## When to Use
- **Queen Orchestrator**: ALWAYS use at session start to create structure and coordinate workers
- **Workers**: Use to check for events, claim tasks, and update status
- **Cross-Worker Communication**: Use when workers need to share state or hand off work
- **Session Resumption**: Use to resume interrupted sessions

## How to Execute

### Step 1: Import and Initialize
```python
from coordination_protocol import CoordinationProtocol

# Initialize (automatically detects project root)
coord = CoordinationProtocol()
```

### Step 2: Session Creation (Queen Only)
```python
# Generate session ID with meaningful task slug
session_id = coord.generate_session_id("implement user authentication API")

# Create session structure
session_path = coord.create_session_structure(
    session_id=session_id,
    task_description="Implement OAuth2 authentication for API",
    complexity_level=3,
    task_type="feature-development"
)

# Log Queen spawn event
coord.log_queen_spawn(session_id, "OAuth2 authentication implementation")
```

### Step 3: Worker Management
```python
# Plan and assign workers
worker_plan = coord.plan_workers(
    task_description="OAuth2 authentication",
    complexity_level=3,
    session_id=session_id
)

# Workers check for events
events = coord.check_events(session_id, last_event_id)

# Update worker status
coord.update_worker_status(session_id, "backend-worker", "in_progress")
```

## Parameters

### Session Creation
- **task_description**: Human-readable task description
- **complexity_level**: 1-4 (simple to complex)
- **task_type**: feature-development, bug-investigation, maintenance-task, integration-project

### Event Management
- **session_id**: Current session identifier
- **worker_name**: Name of the worker (e.g., "backend-worker")
- **event_type**: Type of event (task_claimed, status_update, blocker, handoff)
- **last_event_id**: ID of last processed event (for polling)

## Output

### Directory Structure Created
```
Docs/hive-mind/sessions/{session_id}/
├── SESSION.md           # Session overview and plan
├── STATE.json          # Current session state
├── EVENTS.jsonl        # Event log (append-only)
├── BACKLOG.jsonl       # Task backlog
├── DEBUG.jsonl         # Debug information
├── workers/            # Worker-specific outputs
├── research/           # Research findings
├── archive/            # Completed work archive
└── context/            # Loaded context
```

### Event Format
```json
{
  "id": "evt_001",
  "timestamp": "2024-03-15T14:30:00Z",
  "type": "task_claimed",
  "worker": "backend-worker",
  "data": {
    "task_id": "task_001",
    "description": "Create authentication service"
  }
}
```

## Integration

### Key Methods for Workers

#### Check Events
```python
# Poll for new events
events = coord.check_events(session_id, last_event_id="evt_042")
for event in events:
    if event["type"] == "handoff" and event["target"] == "frontend-worker":
        # Handle handoff from another worker
        handle_handoff(event["data"])
```

#### Update Status
```python
# Update worker status
coord.update_worker_status(
    session_id=session_id,
    worker="backend-worker",
    status="completed",
    details={"endpoints_created": 3, "tests_passing": True}
)
```

#### Log Events
```python
# Log custom event
coord.log_event(
    session_id=session_id,
    event_type="api_ready",
    worker="backend-worker",
    data={"endpoint": "/api/v2/auth", "swagger_url": "/api/docs"}
)
```

### Queen-Specific Methods

#### Worker Planning
```python
# Plan workers based on task complexity
plan = coord.plan_workers(
    task_description="Complex microservices refactor",
    complexity_level=4,
    session_id=session_id
)
# Returns: {"workers": [...], "coordination_strategy": "...", "timeout_config": {...}}
```

#### Session State Management
```python
# Get current session state
state = coord.get_session_state(session_id)

# Update session phase
coord.update_session_phase(session_id, "implementation")
```

## Best Practices

1. **Event Ordering**: Always process events in order by ID
2. **Idempotency**: Make event handlers idempotent (safe to replay)
3. **Frequent Polling**: Workers should check events every 30-60 seconds
4. **Clear Event Types**: Use standardized event types for consistency
5. **Session Path Detection**: Let the protocol auto-detect paths (don't hardcode)

## Error Handling

The protocol handles:
- Project root detection failures (falls back to current directory)
- Concurrent file access (uses file locking for EVENTS.jsonl)
- Missing session directories (auto-creates as needed)
- Invalid complexity levels (defaults to level 2)

## Event Types Reference

### Standard Events
- `queen_spawned`: Session initiated by Queen
- `worker_assigned`: Worker assigned to session
- `task_claimed`: Worker claims specific task
- `status_update`: Worker status change
- `blocker_encountered`: Worker blocked
- `handoff_initiated`: Work passed between workers
- `session_completed`: All work finished

### Worker-Specific Events
- `api_ready`: Backend API endpoints available
- `ui_updated`: Frontend changes deployed
- `tests_completed`: Test suite execution finished
- `research_findings`: Research worker discoveries

## Example: Complete Session Flow

```python
# Queen creates session
coord = CoordinationProtocol()
session_id = coord.generate_session_id("implement payment processing")
session_path = coord.create_session_structure(session_id, "Payment processing", 3)
coord.log_queen_spawn(session_id, "Payment processing feature")

# Plan and assign workers
plan = coord.plan_workers("Payment processing", 3, session_id)

# Backend worker joins
coord.log_event(session_id, "worker_assigned", "backend-worker", 
                {"task": "Create payment API"})

# Backend updates status
coord.update_worker_status(session_id, "backend-worker", "in_progress")

# Backend completes and hands off
coord.log_event(session_id, "handoff_initiated", "backend-worker",
                {"target": "frontend-worker", "data": {"api_docs": "..."}})

# Frontend worker checks events and receives handoff
events = coord.check_events(session_id, None)
# Process handoff event...

# Session completion
coord.update_session_phase(session_id, "completed")
```

## Performance Considerations

- Event log grows append-only (no deletions)
- Use last_event_id to avoid reprocessing
- File locking ensures thread safety
- Auto-rotation for large event logs (>10MB)

## Debugging

Enable debug logging:
```python
coord = CoordinationProtocol()
coord.debug_mode = True  # Writes to DEBUG.jsonl
```

## Notes

- Session IDs must be unique and descriptive (min 15 char slug)
- All timestamps are UTC ISO format
- Event IDs are sequential (evt_001, evt_002, etc.)
- The protocol is thread-safe and supports concurrent workers
- Automatic project root detection works from any subdirectory