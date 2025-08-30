# Hive-Mind Protocol Instructions

These are **instruction protocols** that Queen and Workers should follow during coordination and implementation. They provide step-by-step guidance for using tools (Serena MCP, Read, Write, Edit) to maintain hive-mind coordination through structured files.

## 🎯 Complete Hive-Mind Enhancement System

### ✅ **Task Complexity Assessment with Tag Integration**
- 4-level complexity classification with tag-enhanced analysis
- Automated workflow selection prevents over-engineering simple tasks
- Complexity-appropriate escalation timeout assignment
- Worker context filtering based on tag access matrices

### ✅ **Fast Worker Escalation System**
- Priority-based escalation timeouts: 2min critical, 5min high, 10min medium, 15min low
- Direct worker-to-worker coordination without Queen dependency
- Auto-escalation chains route to domain experts
- Session-integrated escalation state with resumption capability

### ✅ **Complexity-Adaptive Context Loading**
- Single-tag (L1), related-tags (L2), multi-domain (L3-4) memory bank filtering
- Worker-specific tag access matrices with strategic cross-domain access
- 60-80% token efficiency through selective context loading
- Intelligent context caching and sharing optimization

### ✅ **Session Resumption with Memory Bank Context**
- Complete memory bank context preservation and restoration
- Worker context integrity validation across session interruptions
- Conflict resolution for memory bank changes during downtime
- Escalation state restoration with expired escalation handling

### ✅ **Override Persistence System**
- Complexity level overrides persist across sessions with learning
- Worker assignments remain ephemeral (session-only) for flexibility
- Automated learning from override effectiveness with pattern matching
- Task signature-based override application

### ✅ **Enhanced Archive & Reflection System**
- Automatic archive creation on task completion (all complexity levels)
- Complexity-appropriate reflection generation (L2+ tasks)
- Pattern extraction and pattern library contribution (L3+ tasks)
- Session-to-memory-bank learning pipeline with tag integration

## 🎯 IMPORTANT: These Are Instructions, Not Scripts

When you see "commands" in this directory, understand them as:
- **Instruction manuals** for Queen and Workers
- **Protocols to follow** using real tools (Read, Write, Edit)
- **NOT bash scripts** that will auto-execute

## 📋 Available Protocol Instructions

### Core Protocols (Essential)

**session-coordination.md** - Unified session management protocol
- Task complexity assessment (Level 1-4)
- Worker coordination via EVENTS.jsonl
- Escalation protocols and timeouts
- Session resumption and memory bank integration
- Context loading based on complexity

**task-management.md** - Local task management
- Creating tasks with complexity metadata in BACKLOG.jsonl
- Task status monitoring and updates via STATE.json
- Task completion workflows

**research-synthesis.md** - Research coordination
- Context7 research delegation
- Multi-worker research synthesis
- Knowledge base integration

**notification-handler.md** - Worker coordination
- Blocker/unblock event logging
- Cross-worker communication
- Escalation signaling

**pattern-library.md** - Knowledge capture
- Pattern identification and extraction
- Reusable pattern documentation
- Memory bank contribution

### Supporting Protocols

**conflict-resolution.md** - Decision conflicts
**independent-decisions.md** - Worker autonomy
**session-structure.md** - Session file organization

## 🔄 How These Protocols Work

### Example: When Queen needs to synthesize research

1. **Queen reads** `research-synthesis.md` for instructions
2. **Queen uses actual tools** to follow the protocol:
   ```python
   # Read research files
   backend_research = Read("Docs/hive-mind/sessions/1/research/backend/auth.md")
   frontend_research = Read("Docs/hive-mind/sessions/1/research/frontend/ui.md")
   
   # Synthesize findings
   synthesis = combine_findings(backend_research, frontend_research)
   
   # Write synthesis
   Write("Docs/hive-mind/sessions/1/research/README.md", synthesis)
   
   # Save to local memory bank
   Write("Docs/hive-mind/memory-bank/synthesis.md", synthesis)
   ```

### Example: When Worker needs to signal blocker

1. **Worker reads** `notification-handler.md` for instructions
2. **Worker uses actual tools**:
   ```python
   # Append to EVENTS.jsonl
   event = {"ts": timestamp, "type": "blocker", "event": "need_api_ready", "worker": "frontend"}
   Append("Docs/hive-mind/sessions/1/EVENTS.jsonl", event)
   ```

## 🚫 What These Are NOT

- ❌ **NOT executable bash scripts**
- ❌ **NOT commands that run automatically**
- ❌ **NOT something users directly invoke**

## ✅ What These ARE

- ✅ **Step-by-step instructions** for agents
- ✅ **Protocols to ensure consistency** across workers
- ✅ **Reference guides** for complex operations
- ✅ **Documentation** of the hive-mind coordination patterns

## 🎯 Usage Pattern

```
User: "Implement authentication"
  ↓
Queen: Reads summon-queen.md instructions
  ↓
Queen: Follows session creation protocol using local session management
  ↓
Queen: Assigns tasks to workers
  ↓
Workers: Read their agent file instructions
  ↓
Workers: Follow notification-handler.md protocol when blocked
  ↓
Workers: Follow pattern-library.md protocol when pattern found
  ↓
Queen: Follows research-synthesis.md protocol to combine findings
```

All "execution" happens through actual tools (Read, Write, Edit, Bash), not through these instruction files!