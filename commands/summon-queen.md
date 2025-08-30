---
name: summon-queen
description: Launch multi-agent orchestration via the Scribe and Queen agents.
arguments: $ARGUMENTS
---

# 👑 Hive-Mind Orchestration Workflow

This command initiates a new session by first using the `scribe-worker` to create the session, and then activating the `queen-orchestrator` to analyze the task and manage the workers.

## 🚨 WORKFLOW ENFORCEMENT

The `/summon-queen` command follows a strict, two-phase process. You must execute these steps in order.

### Phase 1: Session Creation via Scribe

**Your first action is to spawn the `scribe-worker` to create the session.** Its job is purely mechanical.

**MANDATORY TASK TOOL EXECUTION:**
Use the `Task` tool to spawn the `scribe-worker` with these exact parameters:
- `subagent_type`: "scribe-worker"
- `description`: "Create and initialize a new hive-mind session."
- `prompt`: "Create a session to house the following task description: '$ARGUMENTS'. **Do not analyze the task.** Just create the session files and return the new session_id."

The `scribe-worker` will create the session structure and return a JSON object containing the `session_id`. You must parse this response to get the ID for the next phase.

### Phase 2: Orchestration via Queen

**Once you have the `session_id` from the Scribe, your second action is to spawn the `queen-orchestrator` to perform the strategic analysis.**

**MANDATORY TASK TOOL EXECUTION:**
Use the `Task` tool to spawn the `queen-orchestrator` with these exact parameters:
- `subagent_type`: "queen-orchestrator"
- `description`: "Analyze the session task and orchestrate workers to complete it."
- `prompt`: "Session ID: [session_id_from_scribe]. The session has been prepared. **Your task is to analyze the mandate within the session's STATE.json and begin orchestration.**"

**CRITICAL**: You must pass the `session_id` received from the `scribe-worker` to the `queen-orchestrator`.

---

## Orchestration Lifecycle

1.  **Summon:** You, the top-level agent, receive the `/summon-queen` command.
2.  **Delegate Creation:** You spawn the `scribe-worker` to mechanically create the session.
3.  **Delegate Orchestration:** You spawn the `queen-orchestrator` with the new `session_id` to perform task analysis and worker management.
4.  **Queen Manages:** The Queen plans and manages the specialist workers.
5.  **Delegate Synthesis:** Once the specialist workers are done, the Queen spawns the `scribe-worker` again to synthesize the results.

Your role is to initiate and connect this two-step delegation process correctly, ensuring the roles remain distinct.
