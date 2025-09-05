---
name: summon-queen
description: Launch multi-agent orchestration with session creation and strategic coordination.
arguments: $ARGUMENTS
---

# 👑 Hive-Mind Orchestration Workflow

Launch the hive-mind system: Create session → Queen orchestration → Automatic worker coordination.

## Core Two-Phase Workflow

### Phase 1: Session Creation
Use Bash tool with 5-minute timeout:
```bash
cd .claude
python agents/pydantic_ai/cli.py scribe create --task "$ARGUMENTS" --model custom:max-subscription
```
*Extract `session_id` from JSON response for Phase 2.*

### Phase 2: Queen Orchestration  
Use Bash tool with 5-minute timeout:
```bash
python agents/pydantic_ai/cli.py queen --session [SESSION_ID] --task "$ARGUMENTS" --model custom:max-subscription
```

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

## Phase 3: Claude Code Worker Deployment

**After Queen completes orchestration, YOU (Claude Code) regain control to spawn workers:**

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
1. Navigate to .claude/agents/pydantic_ai/
2. Execute using Bash tool with 5-minute timeout: python cli.py [your-worker-type] --session [SESSION_ID] --task '[YOUR_SPECIFIC_TASK]'
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

## Complete Workflow Success Pattern

```
Task Input → Session Creation → Queen Analysis → 
Dependency Mapping → Shared Contract Creation → 
[Claude Code Regains Control] → Worker Spawning via Task Tool → 
Coordinated Worker Execution → Final Synthesis
```

**Key Innovation**: Queen creates shared agreements upfront + Claude Code orchestrates worker deployment.

## Monitoring Commands

```bash
# Monitor session progress
tail -f Docs/hive-mind/sessions/[SESSION_ID]/EVENTS.jsonl

# Check worker coordination
grep "coordination\|dependency\|contract" Docs/hive-mind/sessions/[SESSION_ID]/EVENTS.jsonl

# Review session state
cat Docs/hive-mind/sessions/[SESSION_ID]/SESSION.md
```

## Success Criteria

- **Pre-Coordination**: All shared interfaces defined before worker execution
- **Dependency Resolution**: No blocking dependencies during execution  
- **Contract Compliance**: Workers follow pre-agreed data formats
- **Clean Synthesis**: Scribe consolidates without design conflicts