---
name: archive-session
description: Archive completed session and extract lessons learned with reflection document
arguments: "$SESSION_ID"
---

# 📦 Archive Hive-Mind Session

Archive completed session **$SESSION_ID** and create comprehensive reflection document.

## Session Archival Protocol

### Step 1: Validate Session Completion
```
Use Read tool to check session status:
Read("Docs/hive-mind/sessions/{session-id}/STATE.json")
Verify session is complete before archiving
```

### Step 2: Create Reflection Document
Use Read and Write tools to synthesize session learnings:

#### Read All Session Data
```
Read("Docs/hive-mind/sessions/{session-id}/SESSION.md") - Session overview
Read("Docs/hive-mind/sessions/{session-id}/EVENTS.jsonl") - All coordination events  
Read("Docs/hive-mind/sessions/{session-id}/BACKLOG.jsonl") - Task completion status
Read("Docs/hive-mind/sessions/{session-id}/notes/*_notes.md") - Worker notes and findings
```

#### Generate Reflection Document Template
```
Write("Docs/hive-mind/sessions/{session-id}/REFLECTION.md", content)
```

**Reflection Document Structure:**
```markdown
# Session Reflection: {session-id}

**Completed**: {timestamp}
**Duration**: {start} to {end}
**Objective**: {original-goal}

## ✅ What Worked Well
- {Successful patterns from EVENTS.jsonl analysis}
- {Effective worker coordination examples}
- {Research findings that accelerated development}
- {Technical decisions that proved correct}

## ❌ What Didn't Work
- {Coordination bottlenecks from EVENTS.jsonl}
- {Research gaps or conflicts}
- {Worker blocking patterns}
- {Technical decisions that needed revision}

## 🧠 Key Learnings
- {Architecture insights}
- {Technology recommendations}
- {Process improvements}
- {Team coordination lessons}

## 📊 Metrics
- **Tasks Completed**: {count from BACKLOG.jsonl}
- **Research Domains**: {count from worker notes}
- **Coordination Events**: {count from EVENTS.jsonl}
- **Conflicts Resolved**: {count of conflict resolution events}
- **Decision Changes**: {count of superseded decisions}

## 🔄 Pattern Library Contributions
- {Reusable patterns discovered}
- {Code templates created}
- {Process improvements}
- {Research methodologies}

## 📝 Recommendations for Future Sessions
- {Process improvements}
- {Tool optimizations}
- {Coordination enhancements}
- {Research methodology refinements}

## 📚 Knowledge Artifacts
- **Research Files**: {list key research outputs}
- **Code Patterns**: {reusable code created}
- **Architecture Decisions**: {key technical choices made}
- **Integration Guides**: {documentation created}
```

### Step 3: Extract Pattern Library Items
```
Use Write tool to save reusable patterns:
Write("Docs/hive-mind/patterns/{pattern-name}.md", pattern_content)
```

**Pattern Categories:**
- **Research Patterns**: Successful Context7 + implementation combinations
- **Coordination Patterns**: Effective worker communication methods
- **Technical Patterns**: Reusable code structures and solutions
- **Process Patterns**: Workflow improvements

### Step 4: Update Session Status
```
Use Edit tool to mark session as archived:
Edit("Docs/hive-mind/sessions/{session-id}/STATE.json",
     old_string: '"status": "completed"',
     new_string: '"status": "archived", "archived_at": "{timestamp}"')
```

### Step 5: Create Archive Summary
```
Use Write tool to create session summary:
Write("Docs/hive-mind/sessions/{session-id}/ARCHIVE_SUMMARY.md", summary)
```

**Archive Summary Structure:**
```markdown
# Archive Summary: {session-id}

**Original Goal**: {objective}
**Outcome**: {success/partial/learning}
**Key Deliverables**: {main outputs}
**Lessons Learned**: {top 3 insights}
**Reusable Artifacts**: {patterns, code, processes}
**Future References**: {when to reference this session}
```

## Integration with Memory Bank

### Step 6: Archive Reflection to Memory Bank
```
Archive learnings to local memory bank:
Write(
  file_path=f"Docs/hive-mind/memory-bank/patterns/{session_id}_learnings.md",
  content=reflection_content
)
```

### Step 7: Update Local Task Records
```
Update local task tracking in BACKLOG.jsonl:
- Mark session tasks as completed
- Record final outcomes and deliverables
- Link to archived session and reflection documents
```

## Quality Gates for Archival

### Required Before Archiving
- [ ] All BACKLOG tasks marked as done or cancelled
- [ ] All EVENTS.jsonl coordination messages resolved
- [ ] Worker notes contain comprehensive findings
- [ ] Independent decisions documented and justified
- [ ] Conflict resolutions (if any) completed

### Archival Completeness
- [ ] Reflection document addresses all session aspects
- [ ] Pattern library updated with reusable items
- [ ] Archon project updated with session outcomes
- [ ] Session files organized and complete
- [ ] Archive summary provides clear session overview

## Future Reference Usage

### When to Reference This Session
- Similar technical challenges arise
- Team coordination patterns needed
- Research methodology questions
- Architecture decision precedents
- Process improvement initiatives

### Search Keywords
Tag reflection with relevant keywords:
- Technology domains used
- Coordination challenges faced  
- Patterns discovered
- Process improvements made

This archival process ensures every session contributes to organizational learning and provides valuable reference material for future hive-mind sessions.
