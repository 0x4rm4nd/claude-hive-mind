# SmartWalletFX Agent Coordination Instructions

> **MANDATORY**: All Claude Code agents must follow these coordination protocols when working on SmartWalletFX tasks.

## 🎯 Agent Spawning Architecture

### **Claude Code Agent → Pydantic AI Agent Chain**

**YOU (Claude Code) do NOT run Pydantic agents directly.** Instead:

1. **You spawn a Claude Agent** using the `Task` tool
2. **That Claude Agent** navigates to `.claude/agents/pydantic_ai/` and executes the Python CLI
3. **The Python CLI** spawns the appropriate Pydantic AI agent with framework-enforced behavior

### **Agent Spawning Process:**

```
Claude Code (you) 
    ↓ (uses Task tool)
Claude Agent (spawned agent)
    ↓ (executes python cli.py)
Pydantic AI Agent (framework-enforced)
    ↓ (returns structured output)
Back to Claude Agent → Back to Claude Code
```

### **Available Pydantic AI Agents**
The spawned Claude Agent will access via: `cd .claude/agents/pydantic_ai/ && python cli.py [agent] [options]`

**Orchestration:**
- **queen**: Complex tasks requiring worker coordination and continuous monitoring
- **scribe**: Session creation and synthesis reports

**Specialist Workers:**
- **analyzer**: Security analysis, performance optimization, code quality
- **architect**: System design, scalability patterns, technical architecture
- **backend**: API development, database design, service implementation
- **designer**: User experience, visual design, accessibility
- **devops**: Infrastructure, deployment, monitoring, CI/CD
- **frontend**: UI/UX implementation, component architecture, state management
- **researcher**: Technical research, best practices, industry standards
- **test**: Testing strategy, quality assurance, coverage analysis

## 🚀 How YOU (Claude Code) Spawn Agents

### **Step 1: Use Task Tool to Spawn Claude Agent**

```
Use Task tool with appropriate subagent_type:
- general-purpose: For most Pydantic AI agent tasks
- [specific-worker]: For targeted domain work (analyzer-worker, backend-worker, etc.)
```

### **Step 2: Claude Agent Executes Pydantic AI Commands**

**For Complex Multi-Domain Tasks:**
The spawned Claude Agent will run:

1. **Create Session First:**
   ```bash
   cd .claude/agents/pydantic_ai/
   python cli.py scribe create --task "YOUR_DETAILED_TASK_DESCRIPTION"
   # Note the returned SESSION_ID
   ```

2. **Use Queen for Orchestration:**
   ```bash
   python cli.py queen --session SESSION_ID --task "TASK_DESCRIPTION" --monitor
   ```

3. **Generate Final Report:**
   ```bash
   python cli.py scribe synthesis --session SESSION_ID
   ```

**For Single-Domain Tasks:**
The spawned Claude Agent will run:
```bash
cd .claude/agents/pydantic_ai/
python cli.py [worker] --session SESSION_ID --task "SPECIFIC_TASK"
```

## 🔄 Model Fallback Strategy

### **Primary Model: Gemini-2.5-Flash**
- All Pydantic AI workers default to `google-gla:gemini-2.5-flash` for optimal performance
- Used for individual worker tasks, analysis, and implementation

### **Queen Model: Gemini-2.5-Pro** 
- Queen orchestrator uses `google-gla:gemini-2.5-pro` for complex reasoning and planning
- Used for strategic task decomposition and worker coordination

### **Scribe Model: GPT-5-Mini**
- Scribe agent uses `openai:gpt-5-mini` for session management and synthesis
- Optimized for session creation and synthesis tasks

### **Fallback Model: OpenAI GPT-5**
- **When to use**: If Gemini quotas exhausted or specific compatibility needed
- **How spawned agents handle**: Manual override with `--model openai:gpt-5`

### **Model Selection Examples:**
```bash
# Queen with Pro model (default)
python cli.py queen --session SESSION_ID --task "TASK" --monitor

# Workers with Flash model (default)  
python cli.py backend --session SESSION_ID --task "TASK"

# Scribe with GPT-5-Mini (default)
python cli.py scribe create --task "TASK"

# Fallback to OpenAI if needed
python cli.py queen --session SESSION_ID --task "TASK" --monitor --model openai:gpt-5
```

## 🛠️ Task Complexity Decision Tree

### **Level 1 - Simple Single-Service Tasks**
**ALWAYS create session first**, then use individual Pydantic worker:
```bash
# Example: Single file edit or simple feature
python cli.py scribe create --task "Fix authentication bug in user service"  
python cli.py backend --session SESSION_ID --task "TASK_DESCRIPTION"
```

### **Level 2 - Service-Specific Complex Tasks**
**Create session first** + use individual Pydantic worker:
```bash
# Example: Complex frontend component with state management
python cli.py scribe create --task "Implement responsive dashboard with real-time portfolio updates"
python cli.py frontend --session SESSION_ID --task "TASK_DESCRIPTION"
```

### **Level 3 - Cross-Service Coordination**
**Use Queen orchestrator** for automatic worker coordination:
```bash
# Example: Feature requiring API + frontend + database changes  
python cli.py scribe create --task "Add portfolio rebalancing feature with real-time notifications"
python cli.py queen --session SESSION_ID --task "TASK_DESCRIPTION" --monitor
```

### **Level 4 - Architecture/Security Reviews**
**Use Queen with specific worker focus**:
```bash
# Example: Comprehensive system analysis
python cli.py scribe create --task "Security audit of crypto-data service focusing on API vulnerabilities and database security"
python cli.py queen --session SESSION_ID --task "TASK_DESCRIPTION" --monitor
```

## 📋 Mandatory Workflow for Claude Code Agents

### **BEFORE starting ANY task using Pydantic AI agents:**

1. **Check Task Complexity** using decision tree above
2. **ALWAYS**: Create session with Scribe first (mandatory for ALL levels)
3. **Level 3+**: Use Queen orchestrator for coordination
4. **Level 4+**: Enable monitoring with Queen

### **Commands the Spawned Claude Agent Will Execute:**

```bash
# Navigate to Pydantic AI directory  
cd .claude/agents/pydantic_ai/

# Create session (MANDATORY for ALL tasks using Pydantic agents)
python cli.py scribe create --task "DETAILED_TASK_DESCRIPTION"

# Use Queen for complex orchestration (Level 3+)
python cli.py queen --session SESSION_ID --task "TASK" --monitor

# Use individual worker for focused tasks
python cli.py [worker] --session SESSION_ID --task "TASK"

# Generate final synthesis report (when work complete)
python cli.py scribe synthesis --session SESSION_ID

# With fallback model if needed
python cli.py [agent] --session SESSION_ID --task "TASK" --model google-gla:gemini-2.5-flash
```

### **Worker Selection Guide:**
- **analyzer**: Security audits, performance optimization, code quality
- **architect**: System design decisions, scalability planning, technical architecture  
- **backend**: API design, database schema, service implementation
- **designer**: UI/UX design, accessibility, visual design systems
- **devops**: Infrastructure, deployment, monitoring, CI/CD setup
- **frontend**: Component development, state management, UI implementation
- **researcher**: Technology evaluation, best practices, industry research
- **test**: Test strategy, quality assurance, coverage analysis

### **Expected Outputs:**
All Pydantic agents return structured, validated data. No unstructured text responses.

## ⚠️ Critical Rules for Claude Code Agents

### **DO NOT (Claude Code Agent Rules):**
- Try to run Pydantic AI commands directly (use Task tool to spawn Claude Agent instead)
- Skip session creation for ANY task using Pydantic agents
- Forget to specify fallback model instructions if GPT-5 might fail
- Try to parse or interpret Pydantic agent outputs (they're pre-structured)

### **ALWAYS (Claude Code Agent Rules):**
- Use Task tool to spawn Claude Agent for Pydantic AI work
- Instruct spawned agent to create session FIRST with `scribe create`
- Include fallback model instructions: "Use `--model google-gla:gemini-2.5-flash` if GPT-5 unavailable"
- Specify Level 3+ tasks should use Queen orchestrator with monitoring
- Request synthesis report when work is complete

### **Session Files Location:**
Results stored in: `Docs/hive-mind/sessions/[SESSION_ID]/`
- `SESSION.md`: Session configuration and documentation
- `EVENTS.jsonl`: Real-time coordination events
- `DEBUG.jsonl`: Debug and execution logs  
- `BACKLOG.jsonl`: Session backlog tracking
- `SYNTHESIS.md`: Final consolidated reports
- `workers/`: Individual worker outputs and notes

## 🔧 Example Task Tool Usage

### **How YOU (Claude Code) Spawn Agents for SmartWalletFX Services:**

**API Service Tasks:**
```
Use Task tool:
subagent_type: backend-worker
prompt: "Navigate to .claude/agents/pydantic_ai/ and run:
1. python cli.py scribe create --task 'Design REST endpoints for crypto portfolio management'
2. python cli.py backend --session SESSION_ID --task 'TASK'
3. Use --model openai:gpt-5 if Gemini unavailable"
```

**Frontend Tasks:**
```
Use Task tool:
subagent_type: frontend-worker  
prompt: "Navigate to .claude/agents/pydantic_ai/ and run:
1. python cli.py scribe create --task 'Implement responsive trading dashboard'
2. python cli.py frontend --session SESSION_ID --task 'TASK'
3. Use --model openai:gpt-5 if Gemini unavailable"
```

**Complex Cross-Service Features:**
```
Use Task tool:
subagent_type: general-purpose
prompt: "Navigate to .claude/agents/pydantic_ai/ and run:
1. python cli.py scribe create --task 'Implement portfolio rebalancing across services'
2. python cli.py queen --session SESSION_ID --task 'TASK' --monitor
3. python cli.py scribe synthesis --session SESSION_ID
4. Use --model google-gla:gemini-2.5-flash if GPT-5 unavailable"
```

**Security Analysis:**
```
Use Task tool:
subagent_type: analyzer-worker
prompt: "Navigate to .claude/agents/pydantic_ai/ and run:
1. python cli.py scribe create --task 'Security analysis of crypto data pipeline'
2. python cli.py analyzer --session SESSION_ID --task 'TASK'  
3. Use --model openai:gpt-5 if Gemini unavailable"
```

---

**These instructions ensure Claude Code agents use the framework-enforced Pydantic AI system for reliable, structured coordination on SmartWalletFX tasks.** ⚡