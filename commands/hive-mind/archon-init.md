---
name: archon-init
description: Initialize Archon integration for new hive-mind session
executor: queen
trigger: automatic on session creation via /summon-queen
arguments: "$SESSION_ID $USER_TASK"
---

# 🏗️ Archon Project Integration

Initializing Archon integration for session **$SESSION_ID**.

## Steps for Queen to Execute Using Real Tools:

### 1. Connect to Archon MCP
**Use Archon MCP tool to get project:**
- Call `mcp__archon__manage_project` with `action="get"` and `project_id="30565f01-937d-433c-b0f0-6960b0dffd93"`
- Verify project exists in response
- If project not found, log fatal error and exit

### 2. Create Tasks Based on User Request
- Analyze user task to determine scope
- Create tasks with service prefixes: [API], [Frontend], [Crypto], [Sara]
- Use embedded checklist format in description:
```markdown
## Implementation Checklist
- [ ] Research best practices
- [ ] Review existing patterns
- [ ] Implement core functionality
- [ ] Write tests
- [ ] Update documentation

## Progress Notes
Session: [session-id]
Research: Docs/hive-mind/sessions/[session-id]/research/
Status: Not started
```

### 3. Initialize Session Directory Structure

**Use Bash tool appropriately to create session directory structure:**

```
Use Bash tool with proper description:
Bash("mkdir -p Docs/hive-mind/sessions/{session-id}/workers/json Docs/hive-mind/sessions/{session-id}/workers/prompts Docs/hive-mind/sessions/{session-id}/notes", 
     description="Create session directory structure")
```

**Create initial session files using Write tool:**
- Create directories by writing placeholder files, then remove placeholders
- Use Write tool for all file creation
- Determine needed research directories based on task analysis

**Research Directory Creation Logic:**
Analyze user task keywords to determine what research directories are needed:
- "backend|API|database" → research/backend/
- "frontend|UI|React" → research/frontend/  
- "design|UX" → research/design/
- "architecture|system" → research/architecture/
- "security|auth" → research/security/
- Only create directories that will be used

**Create research README:**
Use Write tool to create: Docs/hive-mind/sessions/{session-id}/research/README.md
Content: Research index with only relevant topics for this session

### 4. Create STATE.json Using Tools

**Prepare state data structure:**
- session_id: Current session identifier
- archon_project_id: "30565f01-937d-433c-b0f0-6960b0dffd93"
- archon_tasks: Array of created task IDs from step 2
- phase: "research"
- status: "active"
- created_at: Current timestamp

**Create STATE.json file:**
- Try using Serena MCP `write_memory` tool first
- Fallback to Write tool if Serena unavailable
- Use proper JSON formatting with 2-space indentation
- File path: `Docs/hive-mind/sessions/{session_id}/STATE.json`

### 5. Create Simple SESSION.md
```markdown
# Session: [User Task]
**Session ID**: [session-id]
**Status**: Research Phase
**Archon Tasks**: [task-ids]

## Current Focus
[What we're working on]

## Next Steps
[What's next]
```

### 6. Log Initialization Using Write Tool

**Create initial event log entries:**
- Event 1: {"ts": timestamp, "event": "session.created", "session_id": session_id}
- Event 2: {"ts": timestamp, "event": "archon.tasks_created", "tasks": created_task_ids}

**Write events to EVENTS.jsonl:**
- Use Write tool to create file at `Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl`
- Format: One JSON object per line, separated by newlines
- Each event should be a complete JSON object with timestamp

## Summary
This command sets up the minimal structure needed for session management and resumption, with all task tracking delegated to Archon.
