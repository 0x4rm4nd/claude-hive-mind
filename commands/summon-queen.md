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

**Your first action is to run the Pydantic AI scribe to create the session.** This ensures reliable session creation with proper logging.

**MANDATORY BASH EXECUTION:**
Use the `Bash` tool to run the Pydantic AI scribe with these exact parameters:

```bash
cd .claude/agents/pydantic && python cli.py scribe create --task "$ARGUMENTS" --model openai:gpt-5
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
Use the `Bash` tool to run the Pydantic AI Queen orchestrator with these exact parameters:

```bash
cd .claude/agents/pydantic && python cli.py queen --session [session_id_from_scribe] --task "$ARGUMENTS" --model openai:o3
```

The Pydantic AI Queen will:

- Perform intelligent codebase exploration using built-in tools
- Generate comprehensive orchestration plan with worker assignments
- Create detailed worker prompts in the session's `prompts/` directory
- Log all orchestration events automatically to EVENTS.jsonl
- Update SESSION.json with orchestration strategy and assigned workers
- Return structured QueenOrchestrationPlan with complete coordination details

**CRITICAL**: You must pass the exact `session_id` received from the Pydantic AI scribe to the Queen orchestrator.

---

## Orchestration Lifecycle

1.  **Summon:** You, the top-level agent, receive the `/summon-queen` command.
2.  **Run Pydantic Scribe:** You run the Pydantic AI scribe to create the session with guaranteed logging.
3.  **Run Pydantic Queen:** You run the Pydantic AI Queen orchestrator with the new `session_id` to perform intelligent task analysis and worker coordination.
4.  **Deploy Workers:** Use the generated worker prompts and orchestration plan to spawn specialist workers via Task tool.
5.  **Run Pydantic Synthesis:** Once the specialist workers are done, run the Pydantic AI scribe again for synthesis.

Your role is to initiate and connect this two-step delegation process correctly, ensuring the roles remain distinct.
