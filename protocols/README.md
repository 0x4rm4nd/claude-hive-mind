# Hive-Mind Protocols

Instruction protocols and light-weight implementations for Queen and Workers. These files define how agents coordinate, log, and manage sessions using append-only, file-based primitives.

## What These Are
- Step-by-step instructions and reference implementations.
- Consistent conventions for session paths and file formats.
- Append-only coordination via `EVENTS.jsonl`, `DEBUG.jsonl`, and `STATE.json`.

## What These Are Not
- Not auto-executed scripts; agents read and follow them.
- Not a framework; no backward compatibility is maintained.

## Available Protocols (Current Set)

Core implementations (.py):
- `session_management.py` — Unified session paths, append helpers, state updates.
- `coordination_protocol.py` — Session creation, event logging, worker planning.
- `startup_protocol.py` — Startup flow for agents.
- `completion_protocol.py` — Completion and handoff routines.
- `escalation_protocol.py` — Escalation handling.
- `monitoring_protocol.py` — Health and monitoring primitives.
- `synthesis_protocol.py` — Synthesis and consolidation helpers.
- `worker_prompt_protocol.py` — Worker prompt parsing utilities.

Instruction docs (.md):
- `completion_protocol_instructions.md`
- `conflict-resolution.md`
- `coordination_protocol_instructions.md`
- `escalation_protocol_instructions.md`
- `logging_protocol_instructions.md`
- `monitoring_protocol_instructions.md`
- `spawn-protocol.md` — Worker selection and deployment guidelines.
- `spawn-reference.md` — Quick decision guide for Queen orchestrator.
- `startup_protocol_instructions.md`
- `state-management-protocol.md`
- `synthesis_protocol_instructions.md`
- `unified-logging-protocol.md` — Single source of truth for logging via Bash echo.
- `worker-output-protocol.md` — Mandatory output file standards for all workers.
- `worker_prompt_protocol_instructions.md`

Templates (.claude/templates):
- `logging-functions.py` — Canonical `log_event` and `log_debug` (Bash echo append).
- `state-management-functions.py` — Atomic state helpers and validators.
- `state-v2-template.json` — STATE.json template (v2).
- `events.schema.json` — EVENTS.jsonl line schema (this repo).
- `backlog-item-template.json`, `event-template.json`, `debug-entry-template.json`.
- `session-template.md`, `worker-notes-template.md`, `worker-selection-matrix.yaml`.

## Conventions
- Event fields: `timestamp`, `type`, `agent`, `details`, optional `status`.
- Debug fields: `timestamp`, `level`, `agent`, `message`, optional `context`.
- Session ID is implicit from the directory path; NEVER include it in event objects.
- Event types are standardized; NO worker-specific prefixes (use `analysis_started` not `backend_analysis_started`).
- Worker output files: `notes/{worker}_notes.md` and `workers/json/{worker}_response.json` (no "-worker" suffix).
- Appends only; do not overwrite or truncate log files.

## Usage Pattern
1. Queen creates a session with `coordination_protocol.py`.
2. Workers extract the session and IMMEDIATELY log `worker_spawned` event (MANDATORY first event).
3. Workers use `templates/logging-functions.py` for all event/debug logging.
4. All events are appended to `EVENTS.jsonl` using Bash echo (NO session_id in event).
5. Workers create TWO output files: markdown notes and JSON response (see `worker-output-protocol.md`).
6. State updates use atomic write (temp + rename) via `session_management.py`.

Note: Keep it simple. We intentionally avoid lock-heavy concurrency. Append-only design minimizes risk of corruption and is sufficient for our needs.
