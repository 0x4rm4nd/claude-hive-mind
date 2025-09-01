# SmartWalletFX Framework-Enforced Agent System

Production-ready Pydantic AI agents with guaranteed behavior compliance and structured outputs.

## 🏗️ Architecture: Framework-Enforced vs Instruction-Dependent

### **Paradigm Shift**
From hope-based markdown instructions to code-enforced behavior:

| Aspect | Previous (Markdown) | Current (Pydantic AI) |
|--------|-------------------|---------------------|
| **Compliance** | Hope agents follow 500+ line instructions | Framework enforces behavior through code |
| **Outputs** | Unstructured text (requires parsing) | Schema-validated Pydantic models |
| **Debugging** | "Why didn't it follow instructions?" | Python stack traces |
| **Reliability** | Probabilistic behavior | Deterministic code execution |

### **Agent Categories**

**Orchestration & Management:**
- **👑 Queen**: Task coordination with continuous monitoring and schema-validated planning
- **📝 Scribe**: Session lifecycle management and AI-powered synthesis

**Specialized Workers (Framework-Enforced):**
- **🔍 Analyzer**: Security, performance, code quality (→ `AnalyzerOutput`)
- **🏗️ Architect**: System design, scalability patterns (→ `ArchitectOutput`)  
- **⚙️ Backend**: API development, database design (→ `BackendOutput`)
- **🎨 Designer**: UX/UI design, accessibility (→ `DesignerOutput`)
- **🚀 DevOps**: Infrastructure, CI/CD, monitoring (→ `DevOpsOutput`)
- **💻 Frontend**: UI components, state management (→ `FrontendOutput`)
- **🔬 Researcher**: Technical research, best practices (→ `ResearcherOutput`)
- **🧪 Test**: Testing strategy, quality assurance (→ `TestOutput`)

## 🚀 Unified CLI Interface

All agents accessible through single entry point:

```bash
cd .claude/agents/pydantic_ai/
python cli.py [agent] [options]
```

### **Core Workflow**

1. **Create Session** (mandatory for all tasks):
   ```bash
   python cli.py scribe create --task "DETAILED_TASK_DESCRIPTION"  
   ```

2. **Execute Work**:
   - **Simple tasks**: `python cli.py [worker] --session SESSION_ID --task "TASK"`
   - **Complex coordination**: `python cli.py queen --session SESSION_ID --task "TASK" --monitor`

3. **Generate Reports**:
   ```bash
   python cli.py scribe synthesis --session SESSION_ID
   ```

## 📁 Session Management

Framework creates structured sessions in `Docs/hive-mind/sessions/[SESSION_ID]/`:

- **SESSION.md**: Session configuration and documentation
- **EVENTS.jsonl**: Real-time coordination events  
- **DEBUG.jsonl**: Debug and execution logs
- **BACKLOG.jsonl**: Session backlog tracking
- **SYNTHESIS.md**: Final consolidated reports
- **workers/**: Schema-validated individual worker outputs

## 🏗️ Framework-Enforced Protocols

Built-in protocol compliance through Python code:

- **BaseProtocol**: Foundation class with automatic logging
- **ProtocolConfig**: Standardized configuration management
- **SessionManagement**: Session lifecycle automation
- **Event Logging**: Structured logging to EVENTS.jsonl and DEBUG.jsonl

## 🎯 Production Benefits

### **Framework Reliability**
- **100% Schema Compliance**: Impossible to return malformed outputs
- **Automatic Protocol Adherence**: Built into execution flow (cannot skip)
- **Type Safety**: Full Pydantic validation with IDE support
- **Python Stack Traces**: Real debugging instead of instruction-compliance guesswork

### **Operational Efficiency**
- **Single CLI Entry**: Unified interface for all agents
- **Continuous Monitoring**: Real-time worker progress tracking (Queen)
- **AI-Powered Sessions**: Intelligent session ID generation (Scribe)
- **Structured Outputs**: Schema-validated results ready for integration

### **Developer Experience**
- **Easy Extension**: Add new agents without touching existing code
- **Clean Separation**: Agents, shared framework, and protocols isolated
- **Built-in Coordination**: Event logging and session management automatic
- **Scalable Architecture**: Framework handles complexity scaling

## 📁 Directory Structure

```
.claude/
├── agents/
│   ├── pydantic_ai/           # Production framework-enforced agents
│   │   ├── cli.py             # Unified CLI entry point
│   │   ├── queen/             # Orchestrator with continuous monitoring
│   │   ├── scribe/            # Session management and synthesis
│   │   ├── [8-workers]/       # Specialized domain workers
│   │   └── shared/            # Common protocols and utilities
│   ├── archived_agents/       # Legacy markdown agents (superseded)
│   └── README.md              # Agent system documentation
├── commands/                  # User-facing command definitions  
├── README.md                  # This documentation
└── CLAUDE.md                  # Instructions for Claude Code agents
```

## 🚀 Migration Impact

**Legacy System → Production System:**
- Markdown instructions → Framework-enforced Python code
- Hope-based compliance → Guaranteed behavior through code structure  
- Unstructured outputs → Schema-validated Pydantic models
- Manual debugging → Python stack traces with proper error handling

## 🔗 References

- **Pydantic AI KnownModelName**: https://ai.pydantic.dev/api/models/base/#pydantic_ai.models.KnownModelName
  - Official documentation for supported model formats (e.g., `openai:gpt-5`, `google-gla:gemini-2.5-flash`)

---

**Framework-enforced reliability eliminates instruction-compliance issues and ensures predictable, debuggable AI agent coordination.** 🏗️
