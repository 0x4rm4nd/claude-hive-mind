# Agent Coordination Instructions

> **MANDATORY**: All Claude Code agents must follow these coordination protocols when working on tasks.

## 🎯 Agent Spawning Architecture

### **Claude Code Agent → Pydantic AI Agent Chain**

**Agent Execution Patterns:**

**Direct Invocation (Orchestration Agents):**
- **Scribe** and **Queen**: Claude Code agents invoke directly via Python CLI
- Used for session management and complex orchestration tasks

**Spawned Agent Pattern (Worker Agents):**
- **Workers** (analyzer, backend, frontend, etc.): Claude Code spawns Claude Agent using `Task` tool
- That spawned Claude Agent navigates to `.claude/agents/pydantic_ai/` and executes 3-phase workflow
- Used for domain-specific analysis and implementation tasks

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
   python cli.py queen --session SESSION_ID --task "TASK_DESCRIPTION"
   ```

3. **Generate Final Report:**
   ```bash
   python cli.py scribe synthesis --session SESSION_ID
   ```

**For Single-Domain Tasks - 3-Phase Structure:**
The spawned Claude Agent will execute:

```bash
cd .claude/agents/pydantic_ai/

# Phase 1: Setup & Context Loading
python cli.py [worker] --setup --session SESSION_ID

# Phase 2: Direct Analysis (CC Agent executes directly - NO Pydantic)
# CC Agent reads JSON output from Phase 1 and performs analysis using Read/Grep/Glob/Write tools

# Phase 3: Validation & Completion  
python cli.py [worker] --output --session SESSION_ID
```

## 🔄 Model Fallback Strategy

### **Primary Model: custom:max-subscription**

- All Pydantic AI workers default to `custom:max-subscription` for optimal performance
- Used for Phase 1 setup and Phase 3 validation
- Claude Code agents in Phase 2 use their native model (no external model calls)

### **Queen Model: custom:claude-opus-4**  

- Queen orchestrator uses `custom:claude-opus-4` for complex reasoning and planning
- Used for strategic task decomposition and worker coordination

### **Scribe Model: custom:max-subscription**

- Scribe agent uses `custom:max-subscription` for session management and synthesis
- Optimized for session creation and synthesis tasks

### **Fallback Models**

- **Primary fallback**: `custom:max-subscription` for most operations
- **Secondary fallback**: `google-gla:gemini-2.5-flash` if custom models unavailable
- **Emergency fallback**: `openai:gpt-5-mini` for basic operations

### **Model Selection Examples:**

```bash
# Queen with Opus-4 model (default)
python cli.py queen --session SESSION_ID --task "TASK" --model custom:claude-opus-4

# Workers with max-subscription (default)
python cli.py analyzer --setup --session SESSION_ID --task "TASK" --model custom:max-subscription

# Scribe with max-subscription (default)  
python cli.py scribe create --task "TASK" --model custom:max-subscription

# With fallback models if needed
python cli.py analyzer --setup --session SESSION_ID --task "TASK" --model google-gla:gemini-2.5-flash
```

## 🛠️ Task Complexity Decision Tree

### **Level 1-2 - Single-Domain Tasks**
**Use 3-Phase Worker Structure** (analyzer, backend, frontend, etc.):

```bash
# 1. Create session
python cli.py scribe create --task "DETAILED_TASK_DESCRIPTION"
# 2. Execute 3-phase workflow via spawned Claude agent
```

### **Level 3-4 - Cross-Service/Architecture Tasks**  
**Use Queen Orchestrator** with direct invocation:

```bash
# 1. Create session
python cli.py scribe create --task "DETAILED_TASK_DESCRIPTION"
# 2. Queen coordination
python cli.py queen --session SESSION_ID --task "TASK_DESCRIPTION"
# 3. Final synthesis
python cli.py scribe synthesis --session SESSION_ID
```

## 📋 Mandatory 3-Phase Workflow for Claude Code Agents

### **CRITICAL: All Worker Tasks Use 3-Phase Structure**

**Phase 1: Setup & Context Loading (Pydantic AI)**
- Reads Queen-generated prompts from `/workers/prompts/[worker].prompt`  
- Returns structured AnalyzerOutput with prompt data in JSON format
- Prints "WORKER_OUTPUT_JSON:" followed by complete output object

**Phase 2: Direct Analysis & Synthesis (Claude Code Agent)**
- CC Agent extracts Queen's prompt from Phase 1 JSON output
- Performs analysis using Read, Grep, Glob, Write tools DIRECTLY
- NO delegation, NO Task tool usage, NO agent spawning
- Creates required output files (e.g., `analyzer_notes.md`, `analyzer_output.json`)

**Phase 3: Validation & Completion (Pydantic AI)**  
- Validates that analysis files exist and are complete
- Confirms workflow completion and logs final status

### **BEFORE starting ANY task using Pydantic AI agents:**

1. **Check Task Complexity** using decision tree above
2. **ALWAYS**: Create session with Scribe first (mandatory for ALL levels)
3. **Level 3+**: Use Queen orchestrator for coordination
4. **Single-Domain Tasks**: Use 3-phase worker structure

### **Commands the Spawned Claude Agent Will Execute:**

```bash
# Navigate to Pydantic AI directory
cd .claude/agents/pydantic_ai/

# Create session (MANDATORY for ALL tasks using Pydantic agents)
python cli.py scribe create --task "DETAILED_TASK_DESCRIPTION"

# === 3-PHASE WORKER EXECUTION ===

# Phase 1: Setup & Context Loading
python cli.py [worker] --setup --session SESSION_ID --model custom:max-subscription

# Phase 2: Extract JSON data and perform direct analysis
# Parse "WORKER_OUTPUT_JSON:" output from Phase 1
# Extract config.queen_prompt field from JSON
# Execute analysis using Read/Grep/Glob/Write tools DIRECTLY

# Phase 3: Validation & Completion  
python cli.py [worker] --output --session SESSION_ID --model custom:max-subscription

# === COMPLEX ORCHESTRATION ===

# Use Queen for complex orchestration (Level 3+)
python cli.py queen --session SESSION_ID --task "TASK" --model custom:claude-opus-4

# Generate final synthesis report (when work complete)
python cli.py scribe synthesis --session SESSION_ID --model custom:max-subscription
```


## ⚠️ Critical Rules for Claude Code Agents

### **DO NOT (Claude Code Agent Rules):**

- Run worker agents directly (use Task tool to spawn Claude Agent for 3-phase workflow)
- Skip session creation for ANY task using Pydantic agents
- Delegate Phase 2 work to other agents (Claude Code must execute directly)
- Try to parse or interpret Pydantic agent outputs (they're pre-structured)

### **ALWAYS (Claude Code Agent Rules):**

- **Scribe/Queen**: Invoke directly via Python CLI
- **Workers**: Use Task tool to spawn Claude Agent for 3-phase workflow
- Create session FIRST with `scribe create` (mandatory for ALL tasks)
- Include fallback model instructions in spawned agent prompts
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

### **How YOU (Claude Code) Spawn Agents:**

**API Service Tasks:**

```
Use Task tool:
subagent_type: backend-worker
prompt: "Navigate to .claude/agents/pydantic_ai/ and run:
1. python cli.py scribe create --task 'Design REST endpoints for crypto portfolio management'
2. python cli.py backend --setup --session SESSION_ID --model custom:max-subscription
3. Parse JSON output to extract Queen's prompt, then execute direct analysis
4. python cli.py backend --output --session SESSION_ID --model custom:max-subscription
5. Use --model google-gla:gemini-2.5-flash if custom models unavailable"
```

**Frontend Tasks:**

```
Use Task tool:
subagent_type: frontend-worker
prompt: "Navigate to .claude/agents/pydantic_ai/ and run:
1. python cli.py scribe create --task 'Implement responsive trading dashboard'
2. python cli.py frontend --setup --session SESSION_ID --model custom:max-subscription
3. Parse JSON output to extract Queen's prompt, then execute direct analysis
4. python cli.py frontend --output --session SESSION_ID --model custom:max-subscription
5. Use --model google-gla:gemini-2.5-flash if custom models unavailable"
```

**Complex Cross-Service Features (Direct Queen Invocation):**

```bash
# Claude Code invokes directly - NO Task tool needed
cd .claude/agents/pydantic_ai/
python cli.py scribe create --task 'Implement portfolio rebalancing across services'
python cli.py queen --session SESSION_ID --task 'TASK' --model custom:claude-opus-4
python cli.py scribe synthesis --session SESSION_ID --model custom:max-subscription
```

**Security Analysis:**

```
Use Task tool:
subagent_type: analyzer-worker
prompt: "Navigate to .claude/agents/pydantic_ai/ and execute:
1. python cli.py scribe create --task 'Security analysis of crypto data pipeline'
2. python cli.py analyzer --setup --session SESSION_ID --model custom:max-subscription
3. Parse JSON output to extract Queen's prompt, then execute direct analysis
4. python cli.py analyzer --output --session SESSION_ID --model custom:max-subscription
5. Use --model google-gla:gemini-2.5-flash if custom models unavailable"
```

---

**These instructions ensure Claude Code agents use the framework-enforced Pydantic AI system for reliable, structured coordination on differents tasks.** ⚡

## 📖 Additional Context

For comprehensive Pydantic AI agent context including preloaded commands, model configurations, and common patterns, see: `PYDANTIC_AI_CONTEXT.md`

This eliminates the need for spawned agents to analyze structure and enables direct execution.
