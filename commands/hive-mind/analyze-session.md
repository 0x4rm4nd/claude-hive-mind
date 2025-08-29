---
name: analyze-session
description: Comprehensive analysis of session progress, blockers, and remaining work
arguments: "$SESSION_ID"
---

# 📊 Analyze Hive-Mind Session

Performing comprehensive analysis of session **$SESSION_ID**.

## Session Analysis Protocol

### Step 1: Load and Validate Session
**Validate session exists and load context:**

- Check if session directory exists at `Docs/hive-mind/sessions/${SESSION_ID}`
- If not found, list available sessions and exit with error
- Change working directory to session folder
- Generate analysis report header with timestamp and working directory

### Step 2: High-Level Session Overview
**Extract and display session metadata:**

- Read STATE.json to extract: task, status, created_at, updated_at, progress_percentage
- Display key metrics: Task name, current status, creation time, last update, progress percentage
- Calculate session duration using timestamp difference (in hours)
- Format as markdown section with proper headers

### Step 3: Research Phase Analysis
**Analyze research completion status:**

- Read research_complete flag from STATE.json
- Check if RESEARCH_SYNTHESIS.md exists and analyze:
  - File size in lines
  - Last modification time
  - Extract research domains from ## headers
- For each worker type (researcher, backend, frontend, designer, test, devops, analyzer, service-architect):
  - Check if worker notes file exists at `workers/{worker}-worker-notes.md`
  - Count lines of research notes
  - Report activity level per worker

### Step 4: Task Progress Analysis
**Analyze task status and progress if BACKLOG.jsonl exists:**

- Count total tasks in backlog
- Generate task status breakdown (todo, doing, review, done)
- Analyze task priority distribution
- Group tasks by assignee
- List current active tasks (status: "doing")
- Identify and report blocked tasks
- If no backlog file exists, note that session is likely in research phase

### Step 5: Worker Activity Analysis
**Analyze worker status and activity levels:**

- Extract worker states from STATE.json workers section
- For each worker, display status and assigned task
- For each worker notes file in `workers/*.md`:
  - Count lines of activity
  - Show last modification time
  - Display recent activity (last 3 lines) if file has substantial content
  - Format as structured report with activity levels

### Step 6: Communication & Coordination Analysis
**Analyze communication patterns and coordination issues:**

**Event Stream Analysis (if EVENTS.jsonl exists):**
- Count total events
- Break down events by type
- Show recent activity (last 5 events)
- Format as timeline with timestamp, agent, and event type

**Notification Analysis (if NOTIFICATIONS.jsonl exists):**
- Count total notifications
- Break down by notification type
- Show active/recent notifications (last 5)
- Search for blocking issues (blocked_ or critical_blocking patterns)
- Report any critical coordination problems

### Step 7: Quality & Metrics Analysis
**Assess session quality and metrics:**

**Current Metrics (if METRICS.json exists):**
- Display total tasks, completed tasks, average duration, success rate
- Show last update timestamp

**Quality Gates Assessment:**
- Research Phase: Check if research_complete flag is true
- Implementation Progress: Calculate completion rate from BACKLOG.jsonl
  - Count done vs total tasks
  - Calculate percentage completion
- Pattern Library: Check if patterns directory exists and count contributions
  - Look for ../../PATTERNS directory
  - Count .md files as pattern contributions

### Step 8: Bottleneck & Risk Analysis
**Identify and analyze potential issues and bottlenecks:**

**Blocked Task Analysis:**
- Count tasks with status "blocked" in BACKLOG.jsonl
- Report number of blocked tasks if any exist

**Stalled Task Detection:**
- List tasks with status "doing" that may be stalled
- Show task ID, title, and assignee for in-progress tasks

**Worker Load Analysis:**
- Analyze distribution of active tasks across workers
- Identify potentially overloaded workers (>2 active tasks)
- Flag workload imbalances that could cause bottlenecks

### Step 9: Recommendations
**Generate actionable recommendations based on analysis:**

**Phase-Specific Recommendations:**

**Research Phase (if research_complete = false):**
1. Complete pending research: Ensure all Context7 research assignments are finished
2. Synthesize findings: Update RESEARCH_SYNTHESIS.md with unified strategy
3. Validate approach: Review research findings for conflicts or gaps
4. Prepare transition: Ready to create research-informed task breakdown

**Research Phase (if research_complete = true):**
1. Create task breakdown: Use research findings to create BACKLOG.jsonl
2. Set priorities: Establish task priorities based on research dependencies
3. Assign workers: Begin implementation with research-informed assignments
4. Transition phase: Move to implementation_phase

**Implementation Phase:**
1. Resolve blockers: Address any blocked tasks immediately
2. Monitor progress: Review worker activity and task completion rates
3. Coordinate handoffs: Ensure smooth task transitions between workers
4. Quality validation: Verify implementations follow research recommendations

**General Actions (for any phase):**
1. Review session state: Validate current phase and progress
2. Check worker activity: Ensure all workers are coordinated
3. Update documentation: Keep session files current

**Long-term Improvements:**
1. Pattern Documentation: Capture successful approaches in pattern library
2. Metrics Tracking: Monitor and improve task completion times
3. Communication: Enhance worker coordination via notifications
4. Quality Gates: Strengthen research → implementation validation

## Analysis Summary

This comprehensive analysis provides:

- **Session Health**: Overall progress and status assessment
- **Research Quality**: Research completeness and synthesis status
- **Task Progress**: Implementation progress and bottlenecks
- **Worker Coordination**: Activity levels and load distribution
- **Communication Flow**: Event and notification analysis
- **Quality Metrics**: Success rates and completion times
- **Risk Assessment**: Blocked tasks and potential issues
- **Actionable Recommendations**: Specific next steps for improvement

Use this analysis to guide session management decisions and optimize hive-mind coordination.