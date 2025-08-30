# 📋 Hive-Mind Task Management Protocol

Instructions for Queen and Workers on managing tasks through BACKLOG.jsonl and Archon integration.

## Task Management Protocol Instructions

### For Queen: Task Creation and Assignment

**Session Path**: `Docs/hive-mind/sessions/{session-id}/BACKLOG.jsonl`

### Step 1: Check Session Exists
```
Use Read tool: Read("Docs/hive-mind/sessions/{session-id}/SESSION.md")
Verify session exists before managing tasks
```

### Step 2: Review Current Task Status
```
Use Read tool: Read("Docs/hive-mind/sessions/{session-id}/BACKLOG.jsonl")
Check current tasks, priorities, and assignments
```

### Step 3: Create New Tasks
Use Edit tool to append new tasks to BACKLOG.jsonl:

**Task Template**:
```json
{"id": "task-001", "title": "Implement user authentication", "priority": 1, "status": "todo", "assigned_to": "backend-worker", "created_at": "2025-01-15T14:30:00Z", "archon_task_id": "archon-uuid", "dependencies": [], "estimated_hours": 4}
```

**Task Status Flow**:
- `todo` → `in_progress` → `review` → `done`
- `blocked` (special status for dependencies)

### Step 4: Update Archon Integration
For each BACKLOG task, maintain corresponding Archon task:
```
Use mcp__archon__manage_task to sync task status between BACKLOG.jsonl and Archon
```

## For Workers: Task Management

### Step 1: Check Assigned Tasks
```
Use Read tool: Read("Docs/hive-mind/sessions/{session-id}/BACKLOG.jsonl")
Filter for tasks where "assigned_to" matches your worker type
```

### Step 2: Claim Task (Move to in_progress)
```
Use Edit tool to update task status:
Find task by ID, change status from "todo" to "in_progress"
Add "started_at" timestamp
```

### Step 3: Update Progress
```
Use Edit tool to add progress updates:
Update task with progress notes, blockers, or completion status
```

### Step 4: Complete Task
```
Use Edit tool to mark as done:
Change status to "done", add "completed_at" timestamp
```

## Task Operations

### Create Task
```json
{"id": "task-new", "title": "Task description", "priority": 2, "status": "todo", "assigned_to": "worker-type", "created_at": "timestamp", "archon_task_id": "uuid", "dependencies": ["task-001"]}
```

### Update Task Status
```json
{"id": "task-001", "status": "in_progress", "started_at": "timestamp", "progress": "Initial setup complete"}
```

### Block Task
```json
{"id": "task-001", "status": "blocked", "blocker": "waiting for API specification", "blocked_since": "timestamp"}
```

### Complete Task
```json
{"id": "task-001", "status": "done", "completed_at": "timestamp", "deliverables": ["auth-middleware.js", "tests/auth.test.js"]}
```

## Priority Management

### Priority Levels
- **1**: Critical/Blocking - Must be done first
- **2**: High - Important for current iteration  
- **3**: Medium - Standard priority
- **4**: Low - Nice to have
- **5**: Future - Planned but not immediate

### Reordering Tasks
```
Use Edit tool to update priority values
Higher numbers = lower priority
Tasks auto-sort by priority when workers check BACKLOG.jsonl
```

## Integration with EVENTS.jsonl

### Task Status Changes → Events
When updating BACKLOG.jsonl, also log to EVENTS.jsonl:

```json
{"timestamp": "2025-01-15T15:00:00Z", "type": "progress", "event": "task_completed", "agent": "backend-worker", "data": {"task_id": "task-001", "title": "User authentication", "deliverables": ["auth.js"]}}
```

### Task Blocking → Coordination
```json
{"timestamp": "2025-01-15T15:05:00Z", "type": "notification", "event": "task_blocked", "agent": "frontend-worker", "target": "backend-worker", "data": {"blocked_task": "login-ui", "needs": "API endpoint specification", "estimated_delay": "4 hours"}}
```

## Archon Synchronization

### Bidirectional Sync
1. **BACKLOG → Archon**: Local task updates sync to Archon project
2. **Archon → BACKLOG**: Archon task changes reflect in local BACKLOG.jsonl

### Sync Protocol
```
Use mcp__archon__manage_task for all Archon operations
Keep archon_task_id in BACKLOG.jsonl for reference
Update Archon task descriptions with local progress details
```

## Task Dependencies

### Dependency Tracking
```json
{"id": "task-002", "dependencies": ["task-001"], "status": "todo", "can_start": false}
```

### Dependency Resolution
- Tasks with unmet dependencies stay in "todo" status
- When dependency completes, dependent tasks become available
- Use Edit tool to update "can_start": true when dependencies resolve

## Quality Gates

### Task Completion Criteria
- [ ] All acceptance criteria met
- [ ] Code follows project conventions
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Archon task updated with completion details

### Review Process
- Mark tasks as "review" status before "done"
- Include reviewer assignment if needed
- Document review outcomes in task notes

This protocol ensures coordinated task management between hive-mind sessions and Archon project tracking.