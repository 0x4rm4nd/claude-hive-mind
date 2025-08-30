---
name: resume-session
description: Resume existing hive-mind session from interruption or pause
arguments: "$SESSION_ID"
---

# 🔄 Resume Hive-Mind Session

Resuming session **$SESSION_ID** with full context restoration.

## Queen's Session Resumption Protocol

### Step 1: Load Session Context & Memory Bank Integrity Check
```bash
SESSION_ID="$SESSION_ID"
SESSION_DIR="Docs/hive-mind/sessions/${SESSION_ID}"

# Verify session exists
if [ ! -d "${SESSION_DIR}" ]; then
  echo "❌ Session ${SESSION_ID} not found"
  echo "Available sessions:"
  ls -1 Docs/hive-mind/sessions/ 2>/dev/null || echo "No sessions found"
  exit 1
fi

cd "${SESSION_DIR}"
echo "✅ Loading session ${SESSION_ID}"

# Memory Bank Context Integrity Check (using session-coordination.md protocol)
echo ""
echo "## 🧠 Memory Bank Context Restoration"
echo ""

# Get session complexity level and preservation timestamp
COMPLEXITY_LEVEL=$(jq -r '.complexity_level // 2' STATE.json)
PRESERVATION_TIME=$(jq -r '.preservation_timestamp // .updated_at' STATE.json)
DOWNTIME=$(python3 -c "
import datetime
import sys
if sys.argv[1] != 'null':
    preservation = datetime.datetime.fromisoformat(sys.argv[1].replace('Z', '+00:00'))
    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - preservation
    if delta.days > 0:
        print(f'{delta.days} days, {delta.seconds // 3600} hours')
    elif delta.seconds > 3600:
        print(f'{delta.seconds // 3600} hours, {(delta.seconds % 3600) // 60} minutes')
    else:
        print(f'{delta.seconds // 60} minutes')
else:
    print('Unknown')
" "$PRESERVATION_TIME" 2>/dev/null || echo "Unknown")

echo "**Session Downtime**: $DOWNTIME"
echo "**Complexity Level**: $COMPLEXITY_LEVEL"
echo "**Preservation Time**: $PRESERVATION_TIME"

# Check for memory bank changes during downtime
MEMORY_BANK_DIR="../../../../Docs/hive-mind/memory-bank"
if [ -d "$MEMORY_BANK_DIR" ]; then
    echo ""
    echo "**Memory Bank Change Detection**:"
    
    # Check for recent changes in key sections
    RECENT_CHANGES=$(find "$MEMORY_BANK_DIR" -name "*.md" -newer <(date -d "$PRESERVATION_TIME" 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "${PRESERVATION_TIME%+*}" 2>/dev/null || echo "1970-01-01") 2>/dev/null | wc -l)
    
    if [ "$RECENT_CHANGES" -gt 0 ]; then
        echo "⚠️  $RECENT_CHANGES files modified since preservation"
        echo "   Context reload may be required for affected workers"
    else
        echo "✅ No memory bank changes detected - cache restoration viable"
    fi
    
    # List specific changed sections
    find "$MEMORY_BANK_DIR" -name "*.md" -newer <(date -d "$PRESERVATION_TIME" 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%S" "${PRESERVATION_TIME%+*}" 2>/dev/null || echo "1970-01-01") 2>/dev/null | head -5 | while read file; do
        section=$(basename "$file" .md)
        echo "   - $section modified"
    done
else
    echo "⚠️  Memory bank directory not found - using fallback restoration"
fi
```

### Step 2: Analyze Session State
```bash
# Load current session state
echo "## 📊 Session State Analysis"
echo ""

# Check session metadata
echo "### Session Overview"
head -20 SESSION.md

echo ""
echo "### Current State"
cat STATE.json | jq '{
  session_id: .session_id,
  task: .task,
  status: .status,
  current_phase: .current_phase,
  research_complete: .research_complete,
  can_resume: .context.can_resume,
  resume_point: .context.resume_point
}'

echo ""
echo "### Research Progress"
cat STATE.json | jq '.workers'
```

### Step 3: Review Recent Activity
```bash
echo ""
echo "### 📋 Recent Events (Last 10)"
tail -10 EVENTS.jsonl | jq -r '"\(.ts) | \(.agent) | \(.event) | \(.session_id // "N/A")"'

echo ""
echo "### 🔔 Active Notifications"
if [ -s EVENTS.jsonl ]; then
  tail -10 EVENTS.jsonl | jq -r '"\(.timestamp) | \(.from) → \(.to) | \(.type) | \(.urgency)"'
else
  echo "No active notifications"
fi

echo ""
echo "### 📋 Backlog Status"
if [ -s Archon_Tasks_TodoWrite.jsonl ]; then
  echo "Total tasks: $(wc -l < Archon_Tasks_TodoWrite.jsonl)"
  echo ""
  echo "**Status Breakdown**:"
  jq -r '.status' Archon_Tasks_TodoWrite.jsonl | sort | uniq -c | awk '{print "- " $2 ": " $1}'
  
  echo ""
  echo "**Current Tasks in Progress**:"
  jq -r 'select(.status == "doing") | "- \(.id): \(.title) (assignee: \(.assignee))"' Archon_Tasks_TodoWrite.jsonl
else
  echo "No tasks in backlog (research phase)"
fi
```

### Step 4: Worker Context Restoration & Status Assessment
```bash
echo ""
echo "### 👷 Worker Context Restoration"
echo ""

# Determine restoration strategy based on complexity level
case "$COMPLEXITY_LEVEL" in
  1)
    CONTEXT_STRATEGY="minimal"
    CACHE_DURATION="1hour"
    ;;
  2)
    CONTEXT_STRATEGY="standard"
    CACHE_DURATION="4hours"
    ;;
  3)
    CONTEXT_STRATEGY="comprehensive"
    CACHE_DURATION="8hours"
    ;;
  4)
    CONTEXT_STRATEGY="complete"
    CACHE_DURATION="24hours"
    ;;
  *)
    CONTEXT_STRATEGY="standard"
    CACHE_DURATION="4hours"
    ;;
esac

echo "**Context Restoration Strategy**: $CONTEXT_STRATEGY (${CACHE_DURATION} cache)"
echo ""

# Restore worker contexts based on complexity-adaptive approach
for worker_file in notes/*_notes.md; do
  if [ -s "$worker_file" ]; then
    worker_name=$(basename "$worker_file" .md)
    echo "**${worker_name}**:"
    echo "- Last update: $(stat -f "%Sm" "$worker_file" 2>/dev/null || stat -c "%y" "$worker_file" 2>/dev/null || echo "Unknown")"
    echo "- Progress: $(tail -5 "$worker_file" | head -1)"
    
    # Check for preserved worker context state
    if [ -f "context/${worker_name}-context.json" ]; then
      LOADED_TAGS=$(jq -r '.loaded_tags[]?' "context/${worker_name}-context.json" 2>/dev/null | tr '\n' ' ')
      CONTEXT_DEPTH=$(jq -r '.context_depth // "single-tag"' "context/${worker_name}-context.json" 2>/dev/null)
      echo "- Preserved context: $CONTEXT_DEPTH ($LOADED_TAGS)"
      
      # Determine if context reload is needed based on memory bank changes
      if [ "$RECENT_CHANGES" -gt 0 ]; then
        echo "- Restoration: ⚠️  Context reload required (memory bank changes detected)"
      else
        echo "- Restoration: ✅ Cache restoration viable"
      fi
    else
      echo "- Context: Not preserved - will use complexity-appropriate default loading"
    fi
    echo ""
  fi
done

# Display escalation restoration status for Level 3+ sessions
if [ "$COMPLEXITY_LEVEL" -ge 3 ]; then
  echo "**Escalation System Restoration**:"
  if [ -f "escalation-state.json" ]; then
    ACTIVE_ESCALATIONS=$(jq -r 'length' escalation-state.json 2>/dev/null || echo "0")
    echo "- Active escalations to restore: $ACTIVE_ESCALATIONS"
    
    if [ "$ACTIVE_ESCALATIONS" -gt 0 ]; then
      echo "- Escalation timeouts will be recalculated based on preservation time"
      jq -r '.[] | "  - \(.agent) → \(.target): \(.priority) (\(.estimated_delay))"' escalation-state.json 2>/dev/null || echo "  - Unable to parse escalation details"
    fi
  else
    echo "- No preserved escalation state"
  fi
  echo ""
fi
```

### Step 5: Research Status Analysis
```bash
echo "### 🔬 Research Status"
echo ""

if [ -s notes/RESEARCH_SYNTHESIS.md ]; then
  echo "**Research Synthesis Status**:"
  echo "- File size: $(wc -l < notes/RESEARCH_SYNTHESIS.md) lines"
  echo "- Last updated: $(stat -f "%Sm" notes/RESEARCH_SYNTHESIS.md 2>/dev/null || stat -c "%y" notes/RESEARCH_SYNTHESIS.md 2>/dev/null)"
  echo ""
  echo "**Research Domains Covered**:"
  grep "^###" notes/RESEARCH_SYNTHESIS.md | sed 's/^### /- /'
else
  echo "Research synthesis not started"
fi
```

### Step 6: Determine Resume Strategy
```bash
echo ""
echo "## 🎯 Resume Strategy"
echo ""

# Analyze current phase and determine next actions
CURRENT_STATUS=$(jq -r '.status' STATE.json)
RESEARCH_COMPLETE=$(jq -r '.research_complete' STATE.json)

case "$CURRENT_STATUS" in
  "research_phase")
    echo "**Current Phase**: Research"
    echo "**Next Actions**:"
    if [ "$RESEARCH_COMPLETE" = "false" ]; then
      echo "1. Complete pending Context7 research assignments"
      echo "2. Synthesize research findings across workers"
      echo "3. Document unified implementation strategy"
      echo "4. Transition to planning phase"
    else
      echo "1. Review completed research synthesis"
      echo "2. Create research-informed task breakdown"
      echo "3. Initialize Archon_Tasks_TodoWrite.jsonl with implementation tasks"
      echo "4. Transition to implementation phase"
    fi
    ;;
    
  "planning_phase")
    echo "**Current Phase**: Planning"
    echo "**Next Actions**:"
    echo "1. Review task breakdown in Archon_Tasks_TodoWrite.jsonl"
    echo "2. Validate research-informed approach"
    echo "3. Begin worker assignment for implementation"
    echo "4. Transition to implementation phase"
    ;;
    
  "implementation_phase")
    echo "**Current Phase**: Implementation"
    echo "**Next Actions**:"
    echo "1. Review task progress and worker assignments"
    echo "2. Check for blocking notifications"
    echo "3. Continue coordinated implementation"
    echo "4. Monitor quality gates and handoffs"
    ;;
    
  "testing_phase")
    echo "**Current Phase**: Testing"
    echo "**Next Actions**:"
    echo "1. Review test progress and coverage"
    echo "2. Coordinate final quality assurance"
    echo "3. Prepare for session completion"
    ;;
    
  "completed")
    echo "**Current Phase**: Completed"
    echo "**Note**: Session marked as complete"
    echo "**Available Actions**:"
    echo "1. Review session results and patterns"
    echo "2. Archive session if satisfied"
    echo "3. Extend session if additional work needed"
    ;;
    
  *)
    echo "**Current Phase**: Unknown ($CURRENT_STATUS)"
    echo "**Action**: Manual intervention required"
    ;;
esac
```

### Step 7: Update Resume State & Memory Bank Context Integration
```bash
echo ""
echo "## 🔄 Updating Resume State"

RESUME_TIMESTAMP=$(date -Iseconds)

# Update STATE.json with comprehensive resume information
jq --arg timestamp "$RESUME_TIMESTAMP" \
   --arg downtime "$DOWNTIME" \
   --arg strategy "$CONTEXT_STRATEGY" \
   --arg memory_changes "$RECENT_CHANGES" \
   --arg complexity "$COMPLEXITY_LEVEL" '
  .updated_at = $timestamp |
  .context.last_resume = $timestamp |
  .context.resume_count = (.context.resume_count // 0) + 1 |
  .context.downtime = $downtime |
  .context.restoration_strategy = $strategy |
  .context.memory_bank_changes = ($memory_changes | tonumber) |
  .preservation_timestamp = $timestamp |
  .complexity_level = ($complexity | tonumber)
' STATE.json > STATE.tmp && mv STATE.tmp STATE.json

# Create comprehensive resume event log
echo '{
  "ts":"'$RESUME_TIMESTAMP'",
  "agent":"queen",
  "event":"session.resumed",
  "session_id":"'$SESSION_ID'",
  "phase":"'$(jq -r '.status' STATE.json)'",
  "resume_count":"'$(jq -r '.context.resume_count' STATE.json)'",
  "downtime":"'$DOWNTIME'",
  "complexity_level":'$COMPLEXITY_LEVEL',
  "restoration_strategy":"'$CONTEXT_STRATEGY'",
  "memory_bank_changes":'$RECENT_CHANGES',
  "context_integrity":"'$([ "$RECENT_CHANGES" -gt 0 ] && echo "reload_required" || echo "cache_viable")'"
}' >> EVENTS.jsonl

# Create context restoration directories if needed
mkdir -p context escalation

# Preserve current session state for future resumption
echo '{
  "preservation_timestamp":"'$RESUME_TIMESTAMP'",
  "complexity_level":'$COMPLEXITY_LEVEL',
  "restoration_strategy":"'$CONTEXT_STRATEGY'",
  "session_phase":"'$(jq -r '.status' STATE.json)'",
  "worker_states": []
}' > context/preservation-metadata.json

# Update SESSION.md with resumption summary
echo "" >> SESSION.md
echo "## 🔄 Session Resumed: $(date '+%Y-%m-%d %H:%M:%S')" >> SESSION.md
echo "" >> SESSION.md
echo "**Resumption Details**:" >> SESSION.md
echo "- **Downtime**: $DOWNTIME" >> SESSION.md
echo "- **Complexity Level**: $COMPLEXITY_LEVEL ($CONTEXT_STRATEGY context)" >> SESSION.md
echo "- **Memory Bank Changes**: $RECENT_CHANGES files modified" >> SESSION.md
echo "- **Context Strategy**: $([ "$RECENT_CHANGES" -gt 0 ] && echo "Context reload required" || echo "Cache restoration viable")" >> SESSION.md
echo "- **Resume Count**: $(jq -r '.context.resume_count' STATE.json)" >> SESSION.md
echo "" >> SESSION.md

echo "✅ Session state updated with comprehensive resume information"
echo "✅ Memory bank context integration configured"
echo "✅ Worker context restoration strategy determined: $CONTEXT_STRATEGY"

# Display next steps based on restoration requirements
if [ "$RECENT_CHANGES" -gt 0 ]; then
  echo ""
  echo "⚠️  **Action Required**: Memory bank changes detected"
  echo "   - Workers may need context reload for affected tags"
  echo "   - Pattern library access may need refresh"
  echo "   - Cross-worker coordination context should be validated"
fi
```

## Resume Instructions

Based on the analysis above:

### If Research Phase
- **Continue**: Context7 research delegation and synthesis
- **Focus**: Complete research before any implementation
- **Coordinate**: Cross-worker research findings

### If Implementation Phase  
- **Continue**: Task execution with research-informed approach
- **Monitor**: Worker progress and blocking notifications
- **Coordinate**: Task handoffs and quality gates

### If Testing Phase
- **Continue**: Quality assurance and validation
- **Focus**: Research-backed testing strategies
- **Prepare**: Session completion and pattern documentation

## Session Resumption Complete

**Session ${SESSION_ID} successfully resumed!**

**Current Working Directory**: `${SESSION_DIR}`

**Key Files Available**:
- `SESSION.md` - Human-readable session overview
- `STATE.json` - Machine-readable session state  
- `Archon_Tasks_TodoWrite.jsonl` - Task management
- `EVENTS.jsonl` - Complete activity log
- `notes/RESEARCH_SYNTHESIS.md` - Research findings
- `notes/*_notes.md` - Worker-specific progress notes

**Next Step**: Continue with the actions identified in the resume strategy above.
