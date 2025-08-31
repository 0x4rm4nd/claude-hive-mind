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

**When spawned, ALL agents must immediately:**

1. **Load Required Protocols** - Read and follow the specific protocol files referenced in their agent configuration
2. **Complete Startup Sequence** - Execute the mandatory initialization steps defined in `worker-startup-protocol.md`
3. **Maintain Compliance** - Continuously follow protocol requirements throughout task execution
4. **Log All Activities** - Use the standardized logging functions from `unified-logging-protocol.md`

**Key Protocol Categories:**
- **Startup Protocol**: Mandatory initialization sequence for all agents
- **Research Protocol**: Research-first enforcement before implementation
- **Logging Protocol**: Standardized event and debug logging
- **Coordination Protocol**: Inter-agent communication and escalation
- **Session Protocol**: Session management and state tracking

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

### Worker Protocol Compliance

**Each worker agent declares their required protocols in their individual configuration files** (`.claude/agents/[worker-name].md`). When spawned, workers must:

1. **Read their agent configuration** to identify required protocols
2. **Load and follow each protocol** from `.claude/protocols/` directory  
3. **Execute protocol requirements** in the specified order
4. **Maintain compliance** throughout their task execution

**Common Protocol Patterns:**
- All workers follow `worker-startup-protocol.md` and `logging-protocol.md`
- Implementation-focused workers additionally follow `research-protocol.md`
- Coordination-heavy workers additionally follow `coordination-protocol.md`

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
- **Pydantic AI Model 429 Error**: Fallback to `gemini-2.5-flash` model when quota limits hit

## 🔧 Implementation Patterns

### Agent Startup Flow

**All agents follow this high-level startup flow:**

1. **Load Agent Configuration** - Read individual agent file from `.claude/agents/`
2. **Join Active Session** - Locate session directory created by Queen
3. **Execute Startup Protocol** - Follow `worker-startup-protocol.md` requirements exactly
4. **Begin Task Execution** - Start assigned work while maintaining protocol compliance

**Implementation details are defined in the individual protocol files** - agents must reference and follow the specific protocols rather than implementing custom startup logic.

### Protocol Reference

**All event logging, compliance verification, and coordination details are defined in the individual protocol files.** Agents must use the standardized functions provided in:

- `unified-logging-protocol.md` - Event and debug logging functions
- `worker-startup-protocol.md` - Mandatory initialization sequence  
- `coordination-protocol.md` - Inter-agent communication patterns
- `research-protocol.md` - Research-first implementation requirements

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