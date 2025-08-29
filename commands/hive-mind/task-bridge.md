---
name: task-bridge
description: Monitor task progress and sync session state with Archon
executor: queen
trigger: queen-initiated periodically for monitoring (workers update Archon directly)
arguments: "$SESSION_ID"
---

# 🔄 Archon Task Monitoring

Monitor session **$SESSION_ID** task progress in Archon (workers update directly).

## Steps for Queen to Execute:

### 1. Pull Current Task Status from Archon
Since workers update Archon directly, just query current state:

**Query current task status:**
- Call `mcp__archon__manage_task` with `action="list"`
- Use `filter_by="project"` and `filter_value="30565f01-937d-433c-b0f0-6960b0dffd93"`
- Store response for analysis in next steps

### 2. Update SESSION.md with Current Progress
Based on Archon task status:
```markdown
# Session: [Task]
**Status**: Implementation Phase
**Progress**: 60% (12/20 total checklist items done)

## Task Status
- task-001 [Backend]: 3/5 items ✅ (backend-worker)
- task-002 [Frontend]: 2/4 items 🔄 (frontend-worker)  
- task-003 [Test]: 0/3 items ⏳ (unclaimed)

## Next Steps
- Backend: Complete remaining 2 items
- Frontend: Finish component implementation
- Need to assign test task
```

### 3. Identify Bottlenecks
Check for:
- Unclaimed tasks (no assignee)
- Stalled tasks (no recent updates)
- Blocked tasks (in description notes)

### 4. Log Monitoring Event
Add to EVENTS.jsonl:
```json
{"ts":"[timestamp]","event":"archon.monitored","active_tasks":3,"total_progress":"60%"}
```

## Summary
Since workers update Archon directly, this bridge is now just for:
- Monitoring overall progress
- Updating SESSION.md for human readability
- Identifying bottlenecks or unclaimed tasks
- NOT for syncing progress (workers do that themselves)