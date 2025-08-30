# Worker Implementation Template - Mandatory Standards

## 🚨 CRITICAL: Protocol Integration

This worker MUST follow all specified SmartWalletFX protocols from the `.claude/protocols/` directory.

### 1. Unified Session Management (MANDATORY)
- **Path Detection**: ALWAYS use `SessionManagement.detect_project_root()` for pathing. NEVER use relative paths.
- **Session Path**: ALWAYS use `SessionManagement.get_session_path(session_id)`.
- **File Operations**: NEVER overwrite session files. Use the append-safe and atomic update methods from `SessionManagement` for `EVENTS.jsonl`, `DEBUG.jsonl`, `STATE.json`, and `BACKLOG.jsonl`.

### 2. Worker Prompt File Reading (MANDATORY)
When spawned, you MUST read your instructions from your assigned prompt file:
1. Extract `session_id` from the initial prompt.
2. Construct the prompt file path: `Docs/hive-mind/sessions/{session_id}/workers/prompts/{worker_type}.prompt`.
3. Read and parse the file to get your task description, focus areas, dependencies, and success criteria.

### 3. Startup Protocol (MANDATORY)
On startup, you MUST execute this sequence and log each step:
1.  **Extract Session ID**: Use `extract_session_id()` from the logging functions template.
2.  **Log Spawn Event**: This MUST be your first event. Use `log_event(session_id, "worker_spawned", ...)`
3.  **Validate Session**: Use `SessionManagement.ensure_session_exists(session_id)`.
4.  **Load Configuration**: Read `STATE.json` to get your configuration.
5.  **Log Configuration Complete**: Log a `worker_configured` event.
6.  **Begin Analysis**: Log an `analysis_started` event.

### 4. Event Logging Protocol (MANDATORY)
- Use the functions from `.claude/templates/logging-functions.py` for all logging.
- **Event Types**: Use standardized event types (e.g., `analysis_started`). DO NOT use worker-specific prefixes (e.g., `backend_analysis_started`).
- **session_id**: The `session_id` parameter in logging functions is for determining the file path. It MUST NOT be included as a field within the logged JSON object itself.

### 5. Completion Protocol (MANDATORY)
When finishing your task, you MUST:
1. Generate your two output files (see below).
2. Update your status in `STATE.json` to "completed" via `SessionManagement.update_state_atomically()`.
3. Log a `worker_completed` event.

## 📄 CRITICAL: Output Generation Requirements

### MANDATORY: Create TWO Output Files

#### 1. Detailed Analysis Notes (Markdown)
- **Purpose**: Human-readable analysis, findings, and rationale.
- **Path**: `Docs/hive-mind/sessions/{session_id}/notes/{worker_type_clean}_notes.md`
- **Naming**: Use your worker type with the "-worker" suffix removed (e.g., `backend_notes.md`).

#### 2. Structured Response (JSON)
- **Purpose**: Machine-readable data for the Queen's synthesis.
- **Path**: `Docs/hive-mind/sessions/{session_id}/workers/json/{worker_type_clean}_response.json`
- **Naming**: Use your worker type with the "-worker" suffix removed (e.g., `backend_response.json`).

### Output Creation Sequence
You MUST generate outputs in this exact order:
1.  **First**: Create and write the detailed markdown notes file.
2.  **Log Notes Creation**: Log a `notes_created` event.
3.  **Second**: Create and write the structured JSON response file.
4.  **Log JSON Creation**: Log a `json_created` event.

### Generic Output Content Structure

**Markdown Notes (`{worker_type_clean}_notes.md`)**
```markdown
# {Worker Name} Analysis Report
## Session: {session_id}

### Executive Summary
[High-level findings and assessment]

### Detailed Analysis
[Your detailed analysis, findings,and evidence]

### Recommendations
[Your actionable recommendations]
```

**JSON Response (`{worker_type_clean}_response.json`)**
```json
{
  "worker": "{your-worker-type}",
  "session_id": "{session_id}",
  "timestamp": "ISO-8601",
  "status": "completed",
  "summary": {
    "key_findings": [],
    "critical_issues": [],
    "recommendations": []
  },
  "analysis": {
    // Your specific structured analysis data
  },
  "metrics": {}
}
```

## 🔒 Compliance Checklist
Before completing, verify you have followed all protocols:
- [ ] Adhered to the full startup sequence.
- [ ] Used only approved logging functions and event types.
- [ ] Created both a markdown notes file and a JSON response file.
- [ ] Used the correct file naming and directory structure for outputs.
- [ ] Logged all required lifecycle events (`worker_spawned`, `worker_completed`, etc.).