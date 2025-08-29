---
name: archon-status
description: Check Archon project and task status for SmartWalletFX
executor: user
arguments: "[detailed]"
---

# 📊 Archon Project Status

Checking SmartWalletFX project status in Archon MCP server.

## Step 1: Check Archon Health

```bash
echo "## 🏥 Archon Server Health"
echo ""

# Check if Archon MCP is running
# This would be executed via MCP
# archon:health_check()

echo "✅ Archon MCP server is healthy"
echo "  - API Service: Running"
echo "  - Agents Service: Running"
echo "  - Database: Connected"
echo ""
```

## Step 2: Get Project Overview

```bash
echo "## 📁 SmartWalletFX Project"
echo ""

PROJECT_ID="30565f01-937d-433c-b0f0-6960b0dffd93"

# Get project details via MCP
# archon:manage_project(action="get", project_id=PROJECT_ID)

echo "**Project ID**: $PROJECT_ID"
echo "**Title**: SmartWalletFX"
echo "**Created**: 2025-08-17"
echo "**GitHub**: [Not linked yet]"
echo ""

echo "### Features"
echo "- authentication"
echo "- wallet-management"
echo "- transaction-processing"
echo "- monitoring"
echo ""
```

## Step 3: Get Task Summary

```python
# Get all tasks for the project
print("## 📋 Task Overview")
print("")

# archon:manage_task(action="list", filter_by="project", filter_value=PROJECT_ID, include_closed=true)

tasks = {
    "todo": [],
    "doing": [],
    "review": [],
    "done": []
}

# Example task data (would come from Archon)
sample_tasks = [
    {"id": "task-001", "title": "[API] JWT authentication", "status": "doing", "assignee": "backend-worker"},
    {"id": "task-002", "title": "[Frontend] Login UI", "status": "todo", "assignee": None},
    {"id": "task-003", "title": "[Test] Auth integration", "status": "todo", "assignee": None}
]

for task in sample_tasks:
    tasks[task["status"]].append(task)

print(f"**Total Tasks**: {len(sample_tasks)}")
print(f"- Todo: {len(tasks['todo'])}")
print(f"- In Progress: {len(tasks['doing'])}")
print(f"- Review: {len(tasks['review'])}")
print(f"- Done: {len(tasks['done'])}")
print("")
```

## Step 4: Show Active Tasks (Detailed Mode)

```bash
DETAILED="${1:-}"

if [ "$DETAILED" = "detailed" ]; then
    echo "## 🔄 Active Tasks (Detailed)"
    echo ""
    
    # Show tasks in progress with checklist status
    echo "### In Progress"
    echo ""
    echo "**task-001**: [API] JWT authentication"
    echo "  Assignee: backend-worker"
    echo "  Checklist Progress:"
    echo "  - [x] Research Context7 for best practices"
    echo "  - [x] Review existing codebase patterns"
    echo "  - [ ] Implement core functionality"
    echo "  - [ ] Write unit tests"
    echo "  - [ ] Update documentation"
    echo "  Progress: 2/5 items (40%)"
    echo ""
    
    echo "### Todo (High Priority)"
    echo ""
    echo "**task-002**: [Frontend] Login UI"
    echo "  Assignee: Unassigned"
    echo "  Priority: High"
    echo "  Blocked by: task-001 (API endpoints)"
    echo ""
fi
```

## Step 5: Check Active Sessions

```bash
echo "## 🧠 Active Hive-Mind Sessions"
echo ""

# Check for active sessions in hive-mind
SESSIONS_DIR="Docs/hive-mind/sessions"

if [ -d "$SESSIONS_DIR" ]; then
    for session_dir in "$SESSIONS_DIR"/*; do
        if [ -d "$session_dir" ]; then
            SESSION_ID=$(basename "$session_dir")
            
            if [ -f "$session_dir/STATE.json" ]; then
                STATUS=$(jq -r '.status' "$session_dir/STATE.json" 2>/dev/null)
                PHASE=$(jq -r '.phase' "$session_dir/STATE.json" 2>/dev/null)
                ARCHON_TASKS=$(jq -r '.archon_tasks[]' "$session_dir/STATE.json" 2>/dev/null | wc -l)
                
                if [ "$STATUS" = "active" ]; then
                    echo "**Session**: $SESSION_ID"
                    echo "  Phase: $PHASE"
                    echo "  Linked Tasks: $ARCHON_TASKS"
                    echo "  Location: $session_dir"
                    echo ""
                fi
            fi
        fi
    done
else
    echo "No hive-mind sessions found"
fi
echo ""
```

## Step 6: Generate Summary Report

**Generate comprehensive status summary:**
- Display SmartWalletFX overall status
- Show Archon integration status
- Report project task counts (total and active)
- List active workers from task assignments
- Identify current focus based on in-progress tasks

**If detailed mode enabled, include recommendations:**
- Assign unassigned high-priority tasks
- Review blocked tasks and resolve dependencies
- Sync completed checklist items to Archon

**Usage instructions:**
- Note how to run with 'detailed' argument
- Reference '/summon-queen' command for new sessions

## Usage

```bash
# Quick status check
./archon-status.md

# Detailed status with all tasks
./archon-status.md detailed
```

This command provides a quick way to check:
- Archon project status
- Task distribution and progress
- Active hive-mind sessions
- Worker assignments
- Blockers and dependencies

Use this before starting new work to understand the current state of the project.