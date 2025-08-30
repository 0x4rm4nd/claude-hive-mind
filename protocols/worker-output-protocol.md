# Worker Output Protocol - Mandatory File Creation Standards

## Purpose
**AUTHORITATIVE OUTPUT STANDARD** - All workers MUST create specific output files in the exact format and locations specified here. This protocol ensures consistent output across all worker types.

## 🚨 CRITICAL: Mandatory Output Files

### Every Worker MUST Create TWO Output Files

#### 1. Research/Analysis Notes (Markdown)
**Path Format**: `Docs/hive-mind/sessions/{session_id}/workers/{worker_type}_notes.md`
- **Naming**: Use worker type WITHOUT "-worker" suffix (e.g., `backend_notes.md`, `test_notes.md`)
- **Format**: Detailed markdown documentation
- **Purpose**: Human-readable analysis and findings
- **When**: Created during research/analysis phase

#### 2. Structured Response (JSON)
**Path Format**: `Docs/hive-mind/sessions/{session_id}/workers/json/{worker_type}_response.json`
- **Naming**: Use worker type WITHOUT "-worker" suffix (e.g., `backend_response.json`)
- **Format**: Structured JSON for machine processing
- **Purpose**: Queen synthesis and coordination
- **When**: Created after analysis completion

## 📝 File Naming Standards

### Research Phase Files
```python
# CORRECT naming pattern (use underscore, no "-worker")
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/backend_notes.md"
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/test_notes.md"
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/frontend_notes.md"

# INCORRECT (do not use)
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/backend-worker-notes.md"  # Wrong!
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/backend-notes.md"  # Wrong!
```

### JSON Response Files
```python
# CORRECT naming pattern
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/backend_response.json"
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/test_response.json"

# Helper function to get clean worker type
worker_type_clean = WORKER_TYPE.replace('-worker', '')
```

## 📄 Markdown Notes Structure

### Required Sections for ALL Workers
```markdown
# {Worker Type} Analysis Report
## Session: {session_id}
## Generated: {timestamp}

### Executive Summary
[2-3 sentence overview of findings]

### Key Findings
- Finding 1: [Description]
- Finding 2: [Description]
- Finding 3: [Description]

### Detailed Analysis
[Main analysis content specific to worker domain]

### Recommendations
- [Actionable recommendation 1]
- [Actionable recommendation 2]
- [Actionable recommendation 3]

### Dependencies
- [Any dependencies on other workers]
- [Blocking issues identified]

### Next Steps
- [What should happen next]
- [Who should handle it]
```

## 📊 JSON Response Structure

### Required Fields for ALL Workers
```json
{
  "worker": "{worker-type}",
  "session_id": "{session_id}",
  "timestamp": "ISO-8601",
  "status": "completed|blocked|failed",
  "summary": {
    "key_findings": [...],
    "critical_issues": [...],
    "recommendations": [...]
  },
  "analysis": {
    // Worker-specific analysis data
  },
  "metrics": {
    "items_analyzed": 0,
    "issues_found": 0,
    "severity_breakdown": {}
  },
  "dependencies": {
    "requires": [],
    "blocks": [],
    "handoffs": []
  },
  "files_examined": [],
  "files_modified": [],
  "next_actions": []
}
```

## 🔄 Output Creation Sequence

### Mandatory Workflow
```python
# Step 1: Complete analysis/research
findings = perform_analysis()

# Step 2: Create markdown notes FIRST
notes_content = format_markdown_report(findings)
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/{WORKER_TYPE.replace('-worker','')}_notes.md"
Write(notes_path, notes_content)
log_event(session_id, "notes_created", WORKER_TYPE, f"Analysis notes saved to {notes_path}")

# Step 3: Create JSON response SECOND
json_response = format_json_response(findings)
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/{WORKER_TYPE.replace('-worker','')}_response.json"
Write(json_path, json.dumps(json_response, indent=2))
log_event(session_id, "json_created", WORKER_TYPE, "Structured response saved")

# Step 4: Log completion
log_event(session_id, "worker_completed", WORKER_TYPE, f"Analysis complete - {len(findings)} findings")
```

## ⚠️ Common Mistakes to Avoid

### File Naming Errors
- ❌ Including "-worker" in filenames
- ❌ Using hyphens instead of underscores
- ❌ Creating files in wrong directories
- ❌ Missing the json/ subdirectory for JSON files

### Content Errors
- ❌ Creating only one output file (both are required)
- ❌ Creating empty or placeholder files
- ❌ Missing required sections in markdown
- ❌ Missing required fields in JSON

### Timing Errors
- ❌ Creating files before analysis is complete
- ❌ Not logging file creation events
- ❌ Creating JSON before markdown notes

## 🔒 Enforcement Rules

1. **Both Files Required**: Workers failing to create both files will be marked as failed
2. **Naming Convention**: Incorrect file names will cause synthesis failures
3. **Content Validation**: Empty or malformed files will trigger re-execution
4. **Event Logging**: File creation must be logged to EVENTS.jsonl
5. **Directory Structure**: Files must be in correct subdirectories

## 📋 Quick Reference

### File Path Templates
```python
# Research notes (markdown)
notes_path = f"Docs/hive-mind/sessions/{session_id}/workers/{worker_type}_notes.md"

# Structured response (JSON)
json_path = f"Docs/hive-mind/sessions/{session_id}/workers/json/{worker_type}_response.json"

# Helper to clean worker type
worker_type = WORKER_TYPE.replace('-worker', '')
```

### Event Logging for Files
```python
# After creating notes
log_event(session_id, "notes_created", WORKER_TYPE, f"Notes saved: {filename}")

# After creating JSON
log_event(session_id, "json_created", WORKER_TYPE, f"JSON saved: {filename}")
```

## 🎯 Validation Checklist

Before marking task complete, verify:
- [ ] Markdown notes file created in `workers/` directory
- [ ] JSON response file created in `workers/json/` directory
- [ ] Both files use correct naming (no "-worker" suffix)
- [ ] Markdown has all required sections
- [ ] JSON has all required fields
- [ ] File creation events logged
- [ ] Completion event logged

---

**This protocol is THE authoritative standard for worker output file creation.**