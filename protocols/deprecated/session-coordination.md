# Session Coordination Protocol

#session-coordination #complexity #escalation #resumption

## Purpose

Unified protocol for session management, worker coordination, and task complexity handling in the hive-mind system.

## Complexity Assessment

**Determine task complexity (1-4) to drive workflow:**

### Level 1: Simple Task (40% of tasks, < 1 hour)

- Single worker assignment
- Minimal coordination needed
- Standard 15-minute response timeouts

### Level 2: Enhanced Task (30% of tasks, 1-2 hours)

- Research + implementation worker
- Basic coordination via EVENTS.jsonl
- 10-minute escalation timeouts

### Level 3: Cross-Domain Task (20% of tasks, 2-6 hours)

- 2-3 workers with cross-domain coordination
- Active escalation monitoring
- 5-minute escalation timeouts

### Level 4: Complex Project (10% of tasks, 6+ hours)

- 3-5 workers with full coordination
- Comprehensive session management
- 2-minute critical escalation timeouts

## Worker Coordination

**Use EVENTS.jsonl for coordination:**

### Basic Coordination Events

```json
// Worker blocked
{"ts":"timestamp","type":"blocker","agent":"frontend-worker","target":"backend-worker","event":"waiting_for_api","priority":"high"}

// Worker ready/unblocked
{"ts":"timestamp","type":"ready","agent":"backend-worker","target":"frontend-worker","event":"api_ready","resolution":"endpoints available"}

// Task completion
{"ts":"timestamp","type":"completed","agent":"worker-name","task_id":"archon-task-id","deliverables":["file1","file2"]}
```

### Escalation Protocol

1. **Worker blocked** → Log blocker event in EVENTS.jsonl
2. **Timeout exceeded** → Auto-escalate based on complexity timeouts
3. **Escalation received** → Respond within complexity-appropriate timeframe
4. **Resolution** → Log resolution and unblock dependent workers

## Session Structure

**Complexity-appropriate session organization:**

### Basic Session (Level 1-2)

```
sessions/{session-id}/
├── SESSION.md              # Human summary
├── STATE.json              # Machine state
├── EVENTS.jsonl            # Coordination log
└── workers/                # Worker notes
```

### Enhanced Session (Level 3-4)

```
sessions/{session-id}/
├── SESSION.md
├── STATE.json
├── EVENTS.jsonl
├── workers/
├── archive/                # Knowledge capture
└── context/                # Memory bank integration
```

## Session Resumption

**Resume interrupted sessions:**

1. **Load session STATE.json** and check complexity level
2. **Check EVENTS.jsonl** for unresolved escalations
3. **Restore worker context** based on complexity
4. **Resume coordination** with appropriate timeouts

## Memory Bank Integration

**Smart context loading from `Docs/hive-mind/memory-bank/`:**

### Worker Context Loading Steps
**Before starting any task, workers should load relevant context:**

1. **Read Core Project Files**:
   - `activeContext.md` - Current project state and active tasks
   - `techContext.md` - Technology stack and constraints
   - `systemPatterns.md` - Proven architecture patterns
   - `productContext.md` - Business context and goals

2. **Load Domain-Specific Context**:
   - **Backend Worker**: Load archives/reflections tagged with `#backend #api #database #security`
   - **Frontend Worker**: Load archives/reflections tagged with `#frontend #ui #react #ux`
   - **Test Worker**: Load archives/reflections tagged with `#testing #quality #automation`
   - **DevOps Worker**: Load archives/reflections tagged with `#devops #infrastructure #deployment`
   - **Analyzer Worker**: Load archives/reflections tagged with `#security #performance #analysis`
   - **Designer Worker**: Load archives/reflections tagged with `#design #ux #ui #accessibility`
   - **Service Architect**: Load archives/reflections tagged with `#architecture #patterns #scalability`
   - **Researcher Worker**: Load archives/reflections tagged with `#research #documentation #analysis`

3. **Check Recent Context**:
   - Scan last 5 archive files for relevant decisions
   - Check reflection files for lessons learned in your domain

### Context Loading Commands
```bash
# Read core context
core_context=$(cat "Docs/hive-mind/memory-bank/activeContext.md" "Docs/hive-mind/memory-bank/techContext.md")

# Load domain-specific context (example for backend worker)
domain_context=$(grep -l "#backend\|#api\|#database" Docs/hive-mind/memory-bank/archive/*.md | head -5 | xargs cat)
recent_reflections=$(grep -l "#backend\|#api\|#database" Docs/hive-mind/memory-bank/reflection/*.md | head -3 | xargs cat)
```

### Context Preservation

- **Archive decisions** with proper tags for future sessions
- **Extract patterns** from successful implementations
- **Update memory bank** with lessons learned and domain tags

## Implementation Guide

**Follow these steps for session coordination:**

### Queen Orchestrator

1. **Assess complexity** using criteria above
2. **Initialize session** with appropriate structure
3. **Monitor EVENTS.jsonl** for escalations
4. **Coordinate handoffs** between workers
5. **Archive session** with knowledge extraction

### Workers

1. **Check complexity level** from STATE.json
2. **Load appropriate context** from memory bank
3. **Log coordination events** in EVENTS.jsonl
4. **Escalate blockers** with priority levels
5. **Archive contributions** on task completion
