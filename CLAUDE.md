# SmartWalletFX Hive-Mind Coordination System

> **CRITICAL**: This system enforces mandatory protocol compliance for all agents and Queen orchestrator. No steps can be skipped.

## 🎯 Mandatory Agent Initialization

### For ALL Workers and Queen Orchestrator
**BEFORE any task execution, you MUST:**

1. **Protocol Compliance Check**
   - Read your specific agent configuration from `.claude/agents/[your-type].md`
   - Identify required protocols from your agent's `protocols:` field
   - Load protocol instructions from `.claude/protocols/` directory

2. **Session Join** (Workers join existing session created by Queen)
   - Locate active session from `Docs/hive-mind/sessions/` directory
   - Load session context from `STATE.json` 
   - Log worker spawn event to `EVENTS.jsonl`

3. **Protocol Adherence**
   - Complete startup protocol checklist from referenced protocols
   - Update worker status to indicate compliance
   - Begin assigned task execution

## 🔄 Centralized Protocol System

### Protocol Reference Structure
```
.claude/protocols/
├── worker-startup-protocol.md     # ALL agents follow this
├── research-protocol.md           # Research-first enforcement
├── logging-protocol.md            # Event logging standards  
├── coordination-protocol.md       # Inter-agent communication
├── session-coordination.md        # Session management
└── pattern-library.md            # Knowledge patterns
```

### Protocol Enforcement Rules

#### 1. Research-First Protocol (MANDATORY)
**For ALL implementation tasks:**
```markdown
## RESEARCH PHASE [BLOCKING]
□ Search Context7 for best practices and documentation
□ Analyze codebase with Serena tools for existing patterns
□ Review memory bank for relevant implementation patterns
□ Document findings in workers/[agent]-research.md (>500 words)
✓ CHECKPOINT: Research file exists and logged to EVENTS.jsonl

## IMPLEMENTATION PHASE [GATED]  
⚡ GATE: Only proceed after research checkpoint passed
□ Code with research context loaded
□ Log progress every 5 minutes during active coding
```

#### 2. Event Logging Protocol (MANDATORY)
**Smart EVENTS.jsonl Monitoring:**
- **Active Coding**: Suspended during Edit/Write/MultiEdit sequences
- **Coordination Phase**: Check every 2-3 minutes
- **Maximum Silence**: Never exceed 10 minutes without checking
- **Format**: ISO-8601 timestamps, structured JSON

#### 3. Session Coordination Protocol
**Session Structure:**
```
Docs/hive-mind/sessions/{session-id}/
├── STATE.json              # Current execution state
├── EVENTS.jsonl            # Event stream log  
├── DEBUG.jsonl             # Debug information and error logs
├── RESEARCH_SYNTHESIS.md   # Cross-worker findings
└── workers/
    ├── json/               # Worker JSON responses
    ├── notes/              # Worker markdown notes
    └── prompts/            # Worker-specific prompts
```

## 👑 Queen Orchestrator Unique Responsibilities

### Session Management (Queen Only)
- **Session Creation**: Create session directory structure with complexity-appropriate layout
- **Worker Spawning**: Deploy required workers based on task complexity assessment
- **Coordination Oversight**: Monitor cross-worker dependencies and resolve conflicts

### Protocol Compliance Monitoring
- **Real-time Verification**: Analyze STATE.json and EVENTS.jsonl for protocol violations
- **Smart Correction**: Deliver guidance during natural workflow breaks
- **Escalation Resolution**: Handle complex coordination issues requiring arbitration

## 🛠️ Worker Specialization Compliance

### All Workers Must:
1. **Load Domain Context**: Use tag-based filtering for relevant memory bank sections
2. **Follow Startup Protocol**: Complete initialization checklist before task work
3. **Maintain Event Stream**: Log significant operations and coordination needs
4. **Complete Research Phase**: Document findings before implementation
5. **Signal Completion**: Update STATE.json and log completion events

### Worker-Specific Protocol References
```yaml
researcher-worker:
  protocols: [worker-startup-protocol, research-protocol, logging-protocol]
  focus: Context7 research and pattern discovery

architect-worker:
  protocols: [worker-startup-protocol, coordination-protocol, logging-protocol]  
  focus: System design and architecture patterns

backend-worker:
  protocols: [worker-startup-protocol, research-protocol, logging-protocol]
  focus: API and database implementation

frontend-worker:
  protocols: [worker-startup-protocol, coordination-protocol, logging-protocol]
  focus: UI components and state management

designer-worker:
  protocols: [worker-startup-protocol, research-protocol, logging-protocol]
  focus: UX/UI design and accessibility

test-worker:
  protocols: [worker-startup-protocol, coordination-protocol, logging-protocol]
  focus: Testing strategy and quality assurance

devops-worker:
  protocols: [worker-startup-protocol, research-protocol, logging-protocol]
  focus: Infrastructure and deployment

analyzer-worker:
  protocols: [worker-startup-protocol, research-protocol, logging-protocol]
  focus: Security and performance analysis
```

## ⚡ Token Efficiency Optimizations

### Context Loading Strategy
- **Level 1 Tasks**: Single-tag context, minimal session files
- **Level 2 Tasks**: Related-tag context, basic coordination  
- **Level 3 Tasks**: Multi-domain context, cross-worker patterns
- **Level 4 Tasks**: Full context access, comprehensive coordination

### Hard Failure Rules
- **Protocol Violations**: Self-correction required before proceeding
- **Context7/Serena Unavailable**: Graceful degradation to WebSearch + built-in tools
- **Session Corruption**: Create new session if STATE.json/EVENTS.jsonl corrupted

## 🔧 Implementation Patterns

### Worker Startup Sequence Example
```bash
# 1. Load agent configuration
AGENT_TYPE=$(grep "name:" .claude/agents/$(basename $0).md | cut -d' ' -f2)

# 2. Find active session (created by Queen)
SESSION_DIR=$(find "Docs/hive-mind/sessions/" -name "STATE.json" -exec dirname {} \; | head -1)

# 3. Join session and log spawn
echo '{"timestamp":"'$(date -Iseconds)'","type":"worker_spawned","agent":"'$AGENT_TYPE'"}' >> "$SESSION_DIR/EVENTS.jsonl"

# 4. Load and follow required protocols  
for protocol in worker-startup-protocol research-protocol logging-protocol; do
  echo "Following protocol: .claude/protocols/$protocol.md"
done
```

### Event Logging Template
```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "type": "research_complete|task_progress|worker_ready|escalation",
  "agent": "[agent-name]",  
  "session_id": "[session-id]",
  "details": {
    "action": "specific_action_taken",
    "result": "success|in_progress|blocked",
    "metrics": {"tokens_used": 0, "files_modified": 0}
  }
}
```

## 🚨 Compliance Verification

### Self-Correction Process
1. **Violation Detection**: Agent identifies missing protocol steps
2. **Immediate Correction**: Complete missing steps before proceeding
3. **Status Update**: Log correction actions to EVENTS.jsonl
4. **Continue Workflow**: Resume task after compliance restored

### Queen Intervention Triggers
- Missing 2 consecutive EVENTS.jsonl checks during coordination phases  
- Protocol violations detected in STATE.json analysis
- Worker timeout exceeded without escalation event
- Critical priority events ignored for >30 seconds

## 🎯 Success Metrics

### Protocol Compliance KPIs
- **Startup Success Rate**: 100% workers complete initialization
- **Research Coverage**: All implementation tasks have documented research
- **Event Stream Integrity**: No gaps >10 minutes in coordination phases
- **Cross-Worker Sync**: Blocking/unblocking events properly logged

### Operational Efficiency  
- **Token Usage**: 60-80% reduction through selective context loading
- **Coordination Speed**: 40-60% faster blocker resolution
- **Session Resumption**: 90%+ successful restoration after interruptions
- **Knowledge Reuse**: Pattern library reducing research duplication

---

**This CLAUDE.md file ensures consistent protocol adherence across all agents while maintaining the flexibility and efficiency of the hive-mind coordination system.**