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

### Phase 3: Automatic Claude Worker Deployment

**The Queen orchestrator now automatically spawns Claude Worker agents using the Task framework. This establishes the proper hierarchy: Queen → Claude Workers → Pydantic AI Workers.**

**Architecture Flow:**
1. **Queen Analysis Complete**: The Queen has generated the orchestration plan with worker assignments
2. **Automatic Claude Worker Spawning**: The Queen automatically spawns Claude Worker agents (.md files) using the Task tool
3. **Claude Worker Initialization**: Each Claude Worker agent loads its configuration, joins the session, and executes startup protocols
4. **Pydantic AI Worker Spawning**: Each Claude Worker agent then spawns its corresponding Pydantic AI worker
5. **Coordinated Execution**: Workers coordinate through the session event system

**Worker Hierarchy Mapping:**

- `analyzer-worker.md` → `pydantic_ai/analyzer/` - Security, performance, and code quality analysis
- `architect-worker.md` → `pydantic_ai/architect/` - System architecture and design analysis  
- `backend-worker.md` → `pydantic_ai/backend/` - API, database, and service implementation
- `devops-worker.md` → `pydantic_ai/devops/` - Infrastructure, deployment, and operations
- `researcher-worker.md` → `pydantic_ai/researcher/` - Industry standards and best practices research
- `frontend-worker.md` → `pydantic_ai/frontend/` - UI/UX and client-side implementation
- `designer-worker.md` → `pydantic_ai/designer/` - Design patterns and user experience
- `test-worker.md` → `pydantic_ai/test/` - Testing strategies and quality assurance

**No Manual Worker Spawning Required:**
The Queen orchestrator handles all worker spawning automatically through the Task framework. Each Claude Worker agent receives detailed instructions including:

- Session context and coordination requirements
- Specific task focus and priorities
- Protocol compliance checklist
- Instructions to spawn corresponding Pydantic AI worker

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
3.  **Run Pydantic Queen:** You run the Pydantic AI Queen orchestrator with the new `session_id` to perform intelligent task analysis and generate worker assignments.
4.  **Automatic Worker Deployment:** The Queen automatically spawns Claude Worker agents (.md files) using the Task framework. Each Claude Worker then spawns its corresponding Pydantic AI worker, establishing the proper hierarchy: Queen → Claude Workers → Pydantic AI Workers.
5.  **Monitor Progress:** Workers coordinate through the event system, logging progress to EVENTS.jsonl and creating output files in the session directory.
6.  **Run Pydantic Synthesis:** Once the specialist workers are done, run the Pydantic AI scribe again for synthesis.

Your role is to initiate and connect this two-step delegation process correctly, ensuring the roles remain distinct.
