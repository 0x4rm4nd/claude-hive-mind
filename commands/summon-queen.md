---
name: summon-queen
description: Launch multi-agent orchestration via the Scribe and Queen agents.
arguments: $ARGUMENTS
---

# 👑 Hive-Mind Orchestration Workflow

This command initiates a new session by first using the `scribe-worker` to create the session, and then activating the `queen-orchestrator` to analyze the task and manage the workers.

## 🚨 WORKFLOW ENFORCEMENT

The `/summon-queen` command follows a strict, two-phase process. You must execute these steps in order.

### Phase 1: Session Creation via Pydantic AI Scribe

**Your first action is to ensure you're in the .claude directory, then run the Pydantic AI scribe to create the session.** This ensures reliable session creation with proper logging.

**MANDATORY BASH EXECUTION:**
First, navigate to the .claude directory, then use the `Bash` tool to run the Pydantic AI scribe with these exact parameters:

```bash
python agents/pydantic_ai/scribe/runner.py create --task "$ARGUMENTS" --model openai:gpt-5-mini
```

The Pydantic AI scribe will:

- Generate proper session ID in YYYY-MM-DD-HH-mm-shorttaskdescription format
- Create complete session directory structure (no .gitkeep files)
- Log `worker_spawned` and `session_created` events automatically
- Return JSON with `session_id`, `session_path`, and other metadata

Parse the JSON response to extract the `session_id` for the next phase.

### Phase 2: Orchestration via Pydantic AI Queen

**Once you have the `session_id` from the Scribe, your second action is to run the Pydantic AI Queen orchestrator to perform the strategic analysis.**

**MANDATORY BASH EXECUTION:**
From the .claude directory, use the `Bash` tool to run the Pydantic AI Queen orchestrator with these exact parameters:

```bash
python agents/pydantic_ai/queen/runner.py --session [session_id_from_scribe] --task "$ARGUMENTS" --model openai:o3
```

The Pydantic AI Queen will:

- Perform intelligent codebase exploration using built-in tools
- Generate comprehensive orchestration plan with worker assignments
- Create detailed worker prompts in the session's `prompts/` directory
- Log all orchestration events automatically to EVENTS.jsonl
- Update SESSION.json with orchestration strategy and assigned workers
- Return structured QueenOrchestrationPlan with complete coordination details

**CRITICAL**: You must pass the exact `session_id` received from the Pydantic AI scribe to the Queen orchestrator.

### Phase 3: Simultaneous Worker Deployment

**After the Queen has generated the orchestration plan, your third action is to spawn ALL workers simultaneously using parallel Task tool calls.**

**MANDATORY PARALLEL EXECUTION:**
You MUST use a single message with multiple Task tool calls to spawn all workers concurrently. Do NOT spawn workers sequentially one-by-one.

```
Example for 3 workers (analyzer-worker, backend-worker, frontend-worker):

Task tool call 1: analyzer-worker with session_id and task focus
Task tool call 2: backend-worker with session_id and task focus  
Task tool call 3: frontend-worker with session_id and task focus
```

**Worker Spawning Pattern:**
For each worker in the orchestration plan's `worker_assignments`:
1. Extract `worker_type` (e.g., "analyzer-worker") 
2. Extract `task_focus` as the primary task description
3. Use Task tool with:
   - `description`: Short description like "Security analysis task"
   - `prompt`: Full prompt including session_id and task_focus
   - `subagent_type`: The exact worker_type from orchestration plan

**Escalation Handling for Parallel Execution:**
- Workers write escalation events to EVENTS.jsonl when blocked
- Other workers monitor EVENTS.jsonl every 2-3 minutes and respond to escalations
- Peer-to-peer escalation: Direct worker-to-worker coordination before hierarchical escalation
- Queen monitors all activity and resolves complex coordination issues
- Dynamic timeout calculation based on task urgency and domain complexity
- Alternative work routing: Blocked workers continue on non-dependent tasks
- No sequential waiting - all workers start immediately and coordinate via event system

---

## Orchestration Lifecycle

1.  **Summon:** You, the top-level agent, receive the `/summon-queen` command.
2.  **Run Pydantic Scribe:** You run the Pydantic AI scribe to create the session with guaranteed logging.
3.  **Run Pydantic Queen:** You run the Pydantic AI Queen orchestrator with the new `session_id` to perform intelligent task analysis and worker coordination.
4.  **Deploy Workers:** Use the generated worker prompts and orchestration plan to spawn ALL specialist workers SIMULTANEOUSLY via parallel Task tool calls (not sequentially).
5.  **Run Pydantic Synthesis:** Once the specialist workers are done, run the Pydantic AI scribe again for synthesis.

Your role is to initiate and connect this two-step delegation process correctly, ensuring the roles remain distinct.
