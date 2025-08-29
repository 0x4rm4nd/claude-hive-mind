# Session Directory Structure

## Session Creation

**Session ID Format**: `YYYY-MM-DD-HH-MM-{task-name}`
- Example: `2025-01-15-14-30-user-authentication`
- Example: `2025-01-15-16-45-payment-integration`

**Session Directory**: `Docs/hive-mind/sessions/{session-id}/`

## Required Session Files

### Core Coordination Files
```
Docs/hive-mind/sessions/{session-id}/
├── SESSION.md           # Session overview and objectives
├── STATE.json           # Current session state and progress
├── EVENTS.jsonl         # Worker escalation & coordination log (fast response system)
├── Archon_Tasks_TodoWrite.jsonl # Task queue with priorities (managed via Archon and TodoWrite)
└── workers/            # Worker-specific files
    ├── researcher-notes.md      # Research findings and synthesis
    ├── backend-notes.md         # Backend implementation notes
    ├── frontend-notes.md        # Frontend implementation notes
    ├── designer-notes.md        # Design decisions and mockups
    ├── test-notes.md           # Testing strategies and results
    ├── devops-notes.md         # Infrastructure and deployment
    ├── analyzer-notes.md       # Code review and analysis
    ├── architect-notes.md      # Architecture decisions
    └── decisions/              # Independent decision justifications
        ├── backend-decisions.md
        ├── frontend-decisions.md
        ├── test-decisions.md
        └── ...
```

## File Templates

### SESSION.md Template
```markdown
# Session: {task-name}

**Started**: {timestamp}
**Status**: active | paused | completed | archived
**Assigned Queen**: {agent-session-id}

## Objective
{Clear description of what needs to be accomplished}

## Participants
- Queen Orchestrator: {session-id}
- Active Workers: [list of worker types involved]

## Session Timeline
- {timestamp}: Session initialized
- {timestamp}: Research phase started
- {timestamp}: Implementation phase started
- {timestamp}: Testing phase started
- {timestamp}: Session completed

## Current Status
{High-level progress summary}

## Next Actions
- [ ] {action item}
- [ ] {action item}
```

### STATE.json Template
```json
{
  "session_id": "YYYY-MM-DD-HH-MM-{task-name}",
  "created_at": "2025-01-15T14:30:00Z",
  "updated_at": "2025-01-15T16:45:00Z",
  "status": "active",
  "phase": "implementation",
  "archon_project_id": "uuid-here",
  "archon_tasks": [
    {
      "task_id": "uuid",
      "status": "doing",
      "assigned_worker": "backend-worker"
    }
  ],
  "active_workers": [
    "backend-worker",
    "frontend-worker",
    "test-worker"
  ],
  "blocked_workers": [],
  "completed_phases": ["research", "planning"],
  "current_blockers": [],
  "session_metrics": {
    "tasks_completed": 5,
    "tasks_remaining": 3,
    "research_items": 12,
    "decisions_made": 8
  }
}
```

### EVENTS.jsonl Template (Worker Escalation & Coordination)
**Breaking Change**: Fast worker-to-worker coordination system

```jsonl
{"ts": "2025-01-15T14:30:00Z", "type": "session", "agent": "queen-orchestrator", "target": "system", "priority": "medium", "event_id": "session-init-001", "context": "Session initialized: user-authentication"}
{"ts": "2025-01-15T14:31:00Z", "type": "coordination", "agent": "researcher-worker", "target": "system", "priority": "medium", "event_id": "research-001", "context": "Research started: JWT security best practices", "delivery_type": "status_update", "data": {"domain": "authentication", "context7_query": "JWT security best practices"}}
{"ts": "2025-01-15T14:35:00Z", "type": "coordination", "agent": "queen-orchestrator", "target": "backend-worker", "priority": "high", "event_id": "task-assign-001", "context": "Task assigned: implement JWT authentication middleware", "delivery_type": "task_assignment", "data": {"task": "implement-jwt-auth", "archon_task_id": "uuid-here"}}
{"ts": "2025-01-15T14:37:00Z", "type": "blocker", "agent": "frontend-worker", "target": "backend-worker", "priority": "critical", "event_id": "api-spec-blocker-001", "context": "Waiting for API endpoint definition before UI implementation", "escalate_at": "2025-01-15T14:39:00Z", "blocking_tasks": ["create-login-form", "setup-auth-state"]}
{"ts": "2025-01-15T14:38:00Z", "type": "response", "agent": "backend-worker", "target": "frontend-worker", "priority": "critical", "event_id": "api-spec-blocker-001", "context": "Ack, finishing JWT middleware then providing spec", "response_type": "ack", "eta": "2025-01-15T14:42:00Z", "references": ["api-spec-blocker-001"]}
{"ts": "2025-01-15T14:40:00Z", "type": "decision", "agent": "backend-worker", "target": "system", "priority": "low", "event_id": "tech-decision-001", "context": "Independent decision: chose express-jwt over custom implementation", "delivery_type": "decision_log", "data": {"decision": "express-jwt library", "justification_file": "workers/decisions/backend-decisions.md"}}
{"ts": "2025-01-15T14:42:30Z", "type": "coordination", "agent": "backend-worker", "target": "frontend-worker", "priority": "critical", "event_id": "api-spec-blocker-001", "context": "Auth API endpoints ready", "delivery_type": "implementation", "payload": {"endpoints": ["/api/auth/login", "/api/auth/refresh"], "documentation": "Updated in backend-notes.md section 3.1"}, "resolves": ["api-spec-blocker-001"]}
```

**Key Features**:
- **Fast Escalation**: `priority` + `escalate_at` enable timeout-based escalation  
- **Event Tracking**: `event_id` + `resolves` link coordination requests to resolutions
- **Direct Targeting**: `target` field enables worker-to-worker communication
- **Response Protocol**: `response_type` tracks acknowledgment and delivery stages
- **Clean Format**: Streamlined event structure for efficient coordination

### BACKLOG.jsonl Template
```jsonl
{"id": "task-001", "title": "Context7 authentication research", "priority": 1, "status": "completed", "assigned_to": "researcher", "created_at": "2025-01-15T14:30:00Z", "completed_at": "2025-01-15T14:45:00Z"}
{"id": "task-002", "title": "Implement JWT authentication middleware", "priority": 2, "status": "in_progress", "assigned_to": "backend-worker", "created_at": "2025-01-15T14:31:00Z", "archon_task_id": "archon-uuid"}
{"id": "task-003", "title": "Create login UI components", "priority": 3, "status": "pending", "assigned_to": "frontend-worker", "created_at": "2025-01-15T14:32:00Z", "depends_on": ["task-002"]}
```

## Session Lifecycle

### 1. Session Creation
- Queen creates session directory
- Initializes all template files
- Creates Archon project/tasks
- Records session start in EVENTS.jsonl

### 2. Active Session
- Workers update their notes files
- All coordination through EVENTS.jsonl
- Independent decisions logged in decisions/ subdirectory
- Progress tracked in STATE.json and EVENTS.jsonl

### 3. Session Completion
- Final state update
- Archive decision files
- Pattern extraction for library
- Session summary in SESSION.md

### 4. Session Resumption
- Queen loads STATE.json
- Workers read their notes files
- Check EVENTS.jsonl for pending items
- Continue from last known state

## File Management Rules

### Read Before Write
- Always check existing files before creating
- Append to JSONL files, don't overwrite
- Update timestamps in STATE.json

### Coordination Protocol
- Check EVENTS.jsonl before starting new work
- Post to EVENTS.jsonl when blocked or ready
- Update BACKLOG.jsonl when tasks change status

### Decision Documentation
- Independent decisions MUST be justified in decisions/ files
- Include rationale, alternatives considered, impact assessment
- Reference relevant research or constraints