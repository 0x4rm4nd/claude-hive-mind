---
name: research-to-archon
description: Upload research findings to Archon knowledge base for RAG indexing
executor: queen
trigger: after research phase completion
arguments: "$SESSION_ID"
---

# 📚 Research to Archon KB Pipeline

Upload completed research to Archon knowledge base for future RAG retrieval.

## Steps for Queen to Execute:

### 1. Verify Archon Availability

**Check Archon MCP server health:**
- Call `mcp__archon__health_check` to verify server availability
- If health check fails, log fatal error and exit
- CRITICAL: Must fail fast if Archon unavailable

### 2. Collect Research Files
From session directory `Docs/hive-mind/sessions/{session-id}/research/`:
- Backend research findings
- Frontend patterns discovered
- Architecture decisions made
- Security considerations identified

### 3. Upload to Archon KB
**For each research file, upload to knowledge base:**

- Call `mcp__archon__manage_document` with `action="add"`
- Use `project_id="30565f01-937d-433c-b0f0-6960b0dffd93"`
- Set `document_type="research"`
- Set `title="Session {session_id}: {topic}"`
- Include content structure:
  - session_id: Current session identifier
  - topic: Research domain (backend, frontend, etc.)
  - findings: Research content discovered
  - patterns: Extracted patterns for reuse
  - decisions: Key architectural decisions
  - reusable: true (for future RAG queries)
- Add metadata with tags: ["research", topic, session_id]
- Set searchable and rag_indexed flags

### 4. Link to Project Docs
**Update project documentation with research session links:**

- Call `mcp__archon__manage_document` with `action="update"`
- Use `project_id="30565f01-937d-433c-b0f0-6960b0dffd93"`
- Use `doc_id="project-docs"` (main project documentation)
- Update content with research_sessions section:
  - Add current session_id as key
  - Include date, topics array, and kb_references array
  - Link uploaded document IDs for cross-referencing

### 5. Update Archon Tasks
Add research references to task descriptions:
```markdown
## Research References
- KB: research/session-{id}/{topic}
- Local: Docs/hive-mind/sessions/{id}/research/
- Patterns discovered: {count}
- Decisions made: {count}
```

### 6. Log Upload
Add to EVENTS.jsonl:
```json
{"ts":"[timestamp]","event":"research.uploaded_to_archon","docs":3,"session_id":"[id]"}
```

## Benefits
- Research becomes RAG-searchable across all future sessions
- Patterns accumulate in Archon KB
- Both local (for resumption) and Archon (for search) copies
- Future sessions can query: "What did we learn about OAuth?"

## Summary
This creates a learning loop where each session's research enriches the knowledge base, making future development faster and more informed.