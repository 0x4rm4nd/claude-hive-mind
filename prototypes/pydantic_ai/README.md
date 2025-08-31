Pydantic AI Scribe Prototype
============================

This prototype integrates Pydantic AI for the `scribe-worker` to enforce:
- Structured outputs (validated with Pydantic models)
- Deterministic file creation (notes + JSON)
- Mandatory event logging via existing protocols

Files
- `models.py`: Pydantic models for worker output (generic) and scribe synthesis (no scribe notes/JSON).
- `deps.py`: Dependency wiring (session id, worker name, logger).
- `agent_scribe.py`: Pydantic AI agent definition for scribe.
- `run_scribe.py`: Runner to execute the agent in synthesis mode.

Requirements
- Python 3.10+
- Install: `pip install pydantic pydantic-ai`
- Model provider configured (e.g., OpenAI, Anthropic). Set model via `--model` or env.

Usage
- `python -m prototypes.pydantic_ai.run_scribe --session <SESSION_ID> --model <provider:model>`
  - Example: `python -m prototypes.pydantic_ai.run_scribe --session 2025-08-31-12-00-task --model openai:gpt-4o-mini`

Behavior
- Validates session structure with `SessionManagement.ensure_session_exists`.
- Logs `worker_spawned` → runs agent → writes synthesis → logs `synthesis_created`, `synthesis_completed`, `session_completed`, and `worker_completed`.
- Writes:
  - `Docs/hive-mind/sessions/{session_id}/notes/RESEARCH_SYNTHESIS.md`

Notes
- The agent returns validated JSON (`ScribeSynthesisOutput`) including `synthesis_markdown` only.
- The runner writes synthesis and logs events deterministically, independent of LLM compliance.
