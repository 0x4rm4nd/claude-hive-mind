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
python agents/pydantic_ai/queen/runner.py --session [session_id_from_scribe] --task "$ARGUMENTS" --model openai:o3-mini
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

**After the Queen has generated the orchestration plan, your third action is to spawn ALL workers simultaneously using parallel Pydantic AI runner calls.**

**MANDATORY PARALLEL EXECUTION:**
You MUST use a single message with multiple Bash tool calls to spawn all workers concurrently. Do NOT spawn workers sequentially one-by-one.

**Worker Spawning Pattern:**
For each worker in the orchestration plan's `worker_assignments`:

1. Extract `worker_type` (e.g., "analyzer-worker", "backend-worker", "architect-worker")
2. Extract `task_focus` as the primary task description
3. Use Bash tool with `run_in_background: true` to spawn Pydantic AI worker:

```bash
python agents/pydantic_ai/cli.py {worker_name} --session {session_id} --task "{task_focus}" --model openai:gpt-5
```

**Available Pydantic AI Workers:**

- `analyzer` - Security, performance, and code quality analysis
- `architect` - System architecture and design analysis
- `backend` - API, database, and service implementation
- `devops` - Infrastructure, deployment, and operations
- `researcher` - Industry standards and best practices research
- `frontend` - UI/UX and client-side implementation
- `designer` - Design patterns and user experience
- `test` - Testing strategies and quality assurance

**Example Parallel Execution:**

```bash
# Run 3 workers simultaneously using CLI
python agents/pydantic_ai/cli.py analyzer --session 2025-08-31-12-25-crypto-data-analysis --task "Security and Performance Assessment" --model openai:gpt-5 &
python agents/pydantic_ai/cli.py architect --session 2025-08-31-12-25-crypto-data-analysis --task "System Architecture Review" --model openai:gpt-5 &
python agents/pydantic_ai/cli.py backend --session 2025-08-31-12-25-crypto-data-analysis --task "Implementation Analysis" --model openai:gpt-5 &
```

**Monitoring and Coordination:**

- Workers write progress events to `EVENTS.jsonl` automatically
- Workers create output files in `session_directory/workers/notes/`
- Check worker status using: `tail -f Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl`
- Workers coordinate via event system and handle dependencies automatically
- Failed workers will log error events and exit with non-zero status
- Completed workers will log completion events with summary metrics

**Worker Output Structure:**

```
session_directory/
├── EVENTS.jsonl              # Worker progress and coordination events
├── DEBUG.jsonl               # Debug logs and error details
├── SESSION.json              # Session state and orchestration plan
└── workers/
    └── notes/
        ├── analyzer_output.json      # Structured analysis results
        ├── analyzer_notes.md         # Human-readable analysis
        ├── architect_output.json     # Architecture recommendations
        └── ...                       # Other worker outputs
```

---

## Orchestration Lifecycle

1.  **Summon:** You, the top-level agent, receive the `/summon-queen` command.
2.  **Run Pydantic Scribe:** You run the Pydantic AI scribe to create the session with guaranteed logging.
3.  **Run Pydantic Queen:** You run the Pydantic AI Queen orchestrator with the new `session_id` to perform intelligent task analysis and worker coordination.
4.  **Deploy Workers:** Use the orchestration plan to spawn ALL specialist Pydantic AI workers SIMULTANEOUSLY via parallel Bash tool calls with `run_in_background: true` (not sequentially).
5.  **Monitor Progress:** Workers will log their progress to EVENTS.jsonl and create output files in the session directory.
6.  **Run Pydantic Synthesis:** Once the specialist workers are done, run the Pydantic AI scribe again for synthesis.

Your role is to initiate and connect this two-step delegation process correctly, ensuring the roles remain distinct.
