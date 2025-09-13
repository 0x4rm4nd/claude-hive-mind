---
name: summon-queen
description: Launch multi-agent orchestration with session creation and strategic coordination.
arguments: $ARGUMENTS
---

# 👑 Hive-Mind Orchestration Workflow

Launch the hive-mind system: Create session → Queen orchestration → Automatic worker coordination.

## Complete Hive-Mind Orchestration Flow

### Phase 0: Project Root Resolution
Determine absolute paths programmatically:
```bash
# Detect project root (where summon-queen is executed from)
PROJECT_ROOT=$(pwd)
PYDANTIC_AI_PATH="$PROJECT_ROOT/.claude/agents/pydantic_ai"
echo "Project Root: $PROJECT_ROOT"
echo "Pydantic AI Path: $PYDANTIC_AI_PATH"
```

### Phase 1: Session Creation (Scribe Initialization)
Use Bash tool with 5-minute timeout:
```bash
cd "$PYDANTIC_AI_PATH" && python cli.py scribe --create --task "$ARGUMENTS" --model custom:max-subscription
```
*Extract `session_id` from JSON response for Queen orchestration.*

### Phase 2: Strategic Planning (Queen Orchestration)
Use Bash tool with 5-minute timeout:
```bash
cd "$PYDANTIC_AI_PATH" && python cli.py queen --session [SESSION_ID] --task "$ARGUMENTS" --model custom:max-subscription
```

### Phase 3: Worker Deployment & Analysis (Claude Code Coordination)
**After Queen completes orchestration, Claude Code spawns specialized workers using Task tool for cross-domain analysis**

### Phase 4: Creative Synthesis (Scribe Integration)
**Spawn the scribe for creative synthesis of all worker outputs into strategic implementation roadmap**

## Queen's Strategic Responsibilities

### 1. Task Analysis & Dependencies
- Analyze cross-service dependencies (API ↔ Frontend ↔ Backend)
- Map domain boundaries and integration points
- Identify required shared data contracts/interfaces

### 2. Inter-Worker Coordination Planning
**CRITICAL**: Queen must resolve shared interface needs during orchestration:

- **Data Format Agreements**: Define shared JSON schemas, API contracts
- **Component Interfaces**: Specify UI component data requirements  
- **Service Integration**: Create cross-service communication contracts
- **Dependency Ordering**: Sequence workers to avoid blocking dependencies

### 3. Worker Deployment with Contracts
- Spawn workers with pre-agreed shared interfaces
- Include data contracts in worker context
- Establish coordination checkpoints
- Monitor progress and resolve conflicts

## Detailed Phase 3-4 Execution

### Phase 3: Claude Code Worker Deployment & Analysis

**After Queen completes orchestration, Claude Code regains control to spawn workers:**

1. **Parse Queen's Orchestration Plan**: Extract worker assignments from session files
2. **Spawn Workers via Task Tool**: Use Claude Code Task tool with appropriate subagent types
3. **Monitor Coordination**: Track worker progress through session event system

### Worker Spawning Pattern

```javascript
// For each worker in Queen's orchestration plan:
Use Task tool with:
- subagent_type: [worker-type] (e.g., "analyzer-worker", "backend-worker", "frontend-worker")
- prompt: "You are assigned to work on session [SESSION_ID] with the following task from Queen's orchestration plan:

TASK: [SPECIFIC_TASK_FROM_QUEEN]
SESSION: [SESSION_ID] 
SHARED_CONTRACTS: [PRE_ESTABLISHED_DATA_CONTRACTS]

Your responsibility:
1. Resolve project root: PROJECT_ROOT=$(pwd) && PYDANTIC_AI_PATH="$PROJECT_ROOT/.claude/agents/pydantic_ai"
2. Execute using Bash tool with 5-minute timeout: cd "$PYDANTIC_AI_PATH" && python cli.py [your-worker-type] --session [SESSION_ID] --task '[YOUR_SPECIFIC_TASK]'
3. Use --model custom:max-subscription if defaults fail
4. Follow the shared contracts established by Queen
5. Report results back to session coordination system"
```

### Claude Code → Pydantic AI Worker Mapping
- `analyzer-worker` → calls `python cli.py analyzer` - Security, performance analysis
- `architect-worker` → calls `python cli.py architect` - System design, architecture
- `backend-worker` → calls `python cli.py backend` - API, database implementation  
- `frontend-worker` → calls `python cli.py frontend` - UI/UX, component development
- `designer-worker` → calls `python cli.py designer` - Design systems, accessibility
- `devops-worker` → calls `python cli.py devops` - Infrastructure, deployment
- `researcher-worker` → calls `python cli.py researcher` - Technical research, standards
- `test-worker` → calls `python cli.py test` - Testing strategy, quality assurance

### Phase 4: Creative Synthesis (Scribe Integration)

**Phase 4a: Setup Scribe for Creative Synthesis:**

```bash
cd "$PYDANTIC_AI_PATH" && python cli.py scribe --setup --session [SESSION_ID] --model custom:max-subscription
```

**Phase 4b: Generate Final Strategic Implementation Roadmap:**

```bash
cd "$PYDANTIC_AI_PATH" && python cli.py scribe --output --session [SESSION_ID] --model custom:max-subscription
```

**After workers complete, scribe performs multi-phase creative synthesis of all outputs into strategic implementation roadmap with final consolidated report generation.**

## Complete Hive-Mind Workflow Success Pattern

```
Phase 0: Project Root Resolution →
Phase 1: Session Creation (Scribe) →
Phase 2: Strategic Planning (Queen) →
Phase 3: Worker Deployment & Analysis (Claude Code) →
Phase 4a: Creative Synthesis Setup (Scribe --setup) →
Phase 4b: Final Report Generation (Scribe --output) →
Strategic Implementation Roadmap
```

**Key Innovation**: Complete hive-mind orchestration with Queen creating shared agreements, Claude Code coordinating worker deployment, and Scribe providing creative synthesis beyond pattern matching.

## Monitoring Commands

```bash
# Resolve project paths
PROJECT_ROOT=$(pwd)
SESSION_PATH="$PROJECT_ROOT/Docs/hive-mind/sessions/[SESSION_ID]"

# Monitor session progress
tail -f "$SESSION_PATH/EVENTS.jsonl"

# Check worker coordination
grep "coordination\|dependency\|contract" "$SESSION_PATH/EVENTS.jsonl"

# Review session state
cat "$SESSION_PATH/SESSION.md"
```

## Success Criteria

- **Pre-Coordination**: All shared interfaces defined before worker execution
- **Dependency Resolution**: No blocking dependencies during execution  
- **Contract Compliance**: Workers follow pre-agreed data formats
- **Clean Synthesis**: Scribe consolidates without design conflicts