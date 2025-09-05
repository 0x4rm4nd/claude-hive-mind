# Pydantic AI Agent Context - Preloaded for Docker Claude Agents

> **PURPOSE**: This context is automatically loaded for Claude agents running in Docker to eliminate structure analysis and enable direct execution.

## 🚀 Quick Execution Guide

### **Note**: Docker environment automatically handles permissions for Claude CLI execution.

### **Standard Workflow (MANDATORY)**:
```bash
cd /workspace/.claude/agents/pydantic_ai/
python cli.py scribe create --task "TASK_DESCRIPTION"  # Returns SESSION_ID
python cli.py [worker] --session SESSION_ID --task "SPECIFIC_TASK"
python cli.py scribe synthesis --session SESSION_ID  # Generate final report
```

### **Available Agents and Commands**:

#### **Scribe (Session Management)**
```bash
# Create session (ALWAYS FIRST)
python cli.py scribe create --task "Task description"

# Generate synthesis report  
python cli.py scribe synthesis --session SESSION_ID
```

#### **Queen (Orchestration)**
```bash
# Complex multi-worker coordination (Level 3+ tasks)
python cli.py queen --session SESSION_ID --task "TASK" 
```

#### **Specialist Workers**
```bash
# Security analysis, code quality, performance
python cli.py analyzer --session SESSION_ID --task "TASK"

# System architecture, scalability, technical design  
python cli.py architect --session SESSION_ID --task "TASK"

# API development, database design, services
python cli.py backend --session SESSION_ID --task "TASK"

# UI/UX design, accessibility, visual systems
python cli.py designer --session SESSION_ID --task "TASK"

# Infrastructure, deployment, monitoring, CI/CD
python cli.py devops --session SESSION_ID --task "TASK"

# Component development, state management, UI
python cli.py frontend --session SESSION_ID --task "TASK"

# Technical research, best practices, standards
python cli.py researcher --session SESSION_ID --task "TASK"

# Testing strategy, quality assurance, coverage
python cli.py test --session SESSION_ID --task "TASK"
```

## 🔧 Model Configuration (PRELOADED)

### **Current Model Defaults (Updated for Max Subscription)**:
- **Queen**: `custom:claude-opus-4` (Docker Max subscription)
- **Workers**: `google-gla:gemini-2.5-flash` (fallback model)
- **Scribe**: `openai:gpt-5-mini` (session management)

### **Custom Model Names (Route through Docker service on port 47291)**:
- `custom:max-subscription` → Sonnet (via Max subscription)
- `custom:claude-opus-4` → Opus (via Max subscription) 
- `custom:claude-sonnet-4` → Sonnet (via Max subscription)
- `custom:claude-3-7-sonnet` → Sonnet 3.7 (via Max subscription)
- `custom:claude-3-5-haiku` → Haiku (via Max subscription)

### **Fallback Options** (if custom models fail):
```bash
# Use with any command
--model custom:max-subscription
--model custom:claude-sonnet-4
--model google-gla:gemini-2.5-flash
```

## 📁 File Structure (PRELOADED)

### **Session Files Location**: `/workspace/Docs/hive-mind/sessions/[SESSION_ID]/`
- `SESSION.md` - Session configuration and documentation
- `EVENTS.jsonl` - Real-time coordination events
- `DEBUG.jsonl` - Debug and execution logs  
- `BACKLOG.jsonl` - Session backlog tracking
- `SYNTHESIS.md` - Final consolidated reports
- `workers/` - Individual worker outputs and notes

### **Agent Structure**: `/workspace/.claude/agents/pydantic_ai/`
- `cli.py` - Main CLI interface
- `[worker]/` - Individual worker directories
- `shared/` - Shared utilities and protocols
- `queen/` - Orchestration agent
- `scribe/` - Session management agent

## 🎯 Task Complexity Decision Tree (PRELOADED)

### **Level 1** - Simple Single-Service Tasks
**Always create session first**, then use individual worker:
```bash
python cli.py scribe create --task "Fix authentication bug in user service"
python cli.py backend --session SESSION_ID --task "TASK_DESCRIPTION"
```

### **Level 2** - Service-Specific Complex Tasks  
**Create session first** + use individual worker:
```bash
python cli.py scribe create --task "Implement responsive dashboard with real-time updates"
python cli.py frontend --session SESSION_ID --task "TASK_DESCRIPTION"
```

### **Level 3** - Cross-Service Coordination
**Use Queen orchestrator** for automatic worker coordination:
```bash
python cli.py scribe create --task "Add portfolio rebalancing feature with real-time notifications"
python cli.py queen --session SESSION_ID --task "TASK_DESCRIPTION" 
```

### **Level 4** - Architecture/Security Reviews
**Use Queen with specific worker focus**:
```bash
python cli.py scribe create --task "Security audit of crypto-data service focusing on API vulnerabilities"
python cli.py queen --session SESSION_ID --task "TASK_DESCRIPTION" 
```

## ✅ Expected Outputs (PRELOADED)

### **All Pydantic agents return structured, validated JSON data** - not unstructured text.

### **Session Creation Output**:
```json
{
  "session_id": "crypto-security-audit",
  "complexity_level": 4,
  "focus_areas": ["security", "api-analysis", "vulnerability-assessment"],
  "session_files_created": true
}
```

### **Worker Output** (structured):
```json
{
  "analysis": {...},
  "recommendations": [...],
  "implementation_notes": {...},
  "next_steps": [...]
}
```

### **Synthesis Report** (markdown file):
- Integrated analysis from all workers
- Consensus and conflicts identification  
- Actionable insights and recommendations
- Implementation roadmap

## 🚫 Critical Rules for Docker Claude Agents

### **DO NOT**:
- Try to analyze the Pydantic AI structure (context is preloaded)
- Skip session creation (ALWAYS create session first)
- Try to parse or interpret Pydantic agent outputs (they're pre-structured)

### **ALWAYS**:  
- Create session FIRST with `scribe create`
- Include fallback model instructions in prompts
- Specify Level 3+ tasks should use Queen orchestrator with monitoring
- Request synthesis report when work is complete

## 🔍 Testing and Validation

### **Zero API Credit Usage Confirmed**:
- All custom models route through Docker Max subscription
- No API keys used in request path
- All requests confirmed routing through port 47291 Docker service

### **Performance Validated**:
- Response times: 5.9s-14.8s (within acceptable range)
- Zero error rate across all models and workers
- Resource usage: 4.91% memory, 23% CPU (excellent efficiency)

## 📋 Common Usage Patterns

### **Quick Single Worker Test**:
```bash
cd /workspace/.claude/agents/pydantic_ai/
python cli.py scribe create --task "Test backend API endpoints"
SESSION_ID="test-backend-api"
python cli.py backend --session $SESSION_ID --task "Analyze REST API security"
python cli.py scribe synthesis --session $SESSION_ID
```

### **Complex Multi-Worker Analysis**:
```bash
cd /workspace/.claude/agents/pydantic_ai/  
python cli.py scribe create --task "Comprehensive crypto-data service analysis"
SESSION_ID="crypto-service-analysis"
python cli.py queen --session $SESSION_ID --task "Full analysis including security, performance, scalability" 
python cli.py scribe synthesis --session $SESSION_ID
```

### **With Fallback Models**:
```bash
# If custom models fail, use fallback
python cli.py queen --session $SESSION_ID --task "TASK"  --model custom:max-subscription
```

---

**This context eliminates the need for structure analysis and enables direct execution of Pydantic AI workflows in the Docker environment.** 🚀