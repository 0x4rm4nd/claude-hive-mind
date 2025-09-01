# Agent Configurations

Production-ready agent definitions for the hive-mind orchestration system.

## 🚀 **Migration Complete: Framework-Enforced AI**

**All agents have been successfully migrated to Pydantic AI** - moving from instruction-dependent behavior to framework-enforced reliability through code validation.

## Agent Architecture

### 🏗️ **Framework-Enforced Agents (Pydantic AI)** - Production Ready

**Orchestration & Management:**

- **pydantic/queen/**: Master coordinator with continuous monitoring ([Full Documentation](pydantic/README.md))
- **pydantic/scribe/**: Session creation and synthesis management

**Worker Specialists (8 Complete):**

- **pydantic/analyzer/**: Security analysis, performance optimization, code quality assessment
- **pydantic/architect/**: System design, scalability patterns, technical architecture
- **pydantic/backend/**: API development, database design, service implementation
- **pydantic/designer/**: User experience design, visual design, accessibility
- **pydantic/devops/**: Infrastructure, deployment, monitoring, CI/CD pipelines
- **pydantic/frontend/**: UI/UX implementation, component architecture, state management
- **pydantic/researcher/**: Technical research, best practices, industry standards analysis
- **pydantic/test/**: Testing strategy, quality assurance, test coverage analysis

### 🏗️ **Meta-Development**

- **agent-architect.md**: Pydantic AI expert for designing framework-enforced agent architectures

### 📚 **Archived Legacy Agents**

- **archived/**: Contains all previous Markdown-based agent definitions
  - `queen-orchestrator.md` (superseded by `pydantic/queen/`)
  - 8 worker agents (superseded by `pydantic/[worker]/` implementations)

## 🚀 **Usage - Unified CLI Interface**

All agents are now accessible through a single CLI entry point:

```bash
cd .claude/agents/pydantic_ai/
python cli.py [agent] [options]
```

### **Orchestration & Session Management**

```bash
# Create session with AI-powered session ID
python cli.py scribe create --task "Analyze crypto-data architecture focusing on security"

# Run Queen orchestrator with continuous monitoring
python cli.py queen --session SESSION_ID --task "..." --monitor

# Generate final synthesis from completed workers
python cli.py scribe synthesis --session SESSION_ID
```

### **Worker Agents**

```bash
# Security, performance, and code quality analysis
python cli.py analyzer --session SESSION_ID --task "Security audit of crypto-data service"

# System design and architecture review
python cli.py architect --session SESSION_ID --task "Review scalability patterns"

# API and database implementation
python cli.py backend --session SESSION_ID --task "Design API endpoints"

# UX/UI design and accessibility
python cli.py designer --session SESSION_ID --task "Design user dashboard"

# Infrastructure and deployment
python cli.py devops --session SESSION_ID --task "Setup monitoring infrastructure"

# Frontend development and optimization
python cli.py frontend --session SESSION_ID --task "Implement responsive components"

# Technical research and best practices
python cli.py researcher --session SESSION_ID --task "Research React patterns"

# Testing strategy and quality assurance
python cli.py test --session SESSION_ID --task "Design test coverage strategy"
```

## 🔧 **Framework Benefits**

### **Before (Markdown Instructions)**

- ❌ Hope agents follow 500+ line instructions
- ❌ Unstructured output (can return anything)
- ❌ Manual protocol compliance (error-prone)
- ❌ Debugging: "Why didn't it follow instructions?"

### **After (Framework-Enforced)**

- ✅ Code-enforced behavior (impossible to ignore)
- ✅ Schema-validated output (Pydantic models only)
- ✅ Built-in protocol compliance (automatic)
- ✅ Python stack traces for debugging

### **Structured Output Examples**

```python
# Analyzer Output
class AnalyzerOutput(BaseModel):
    security_findings: List[SecurityFinding]
    performance_issues: List[PerformanceIssue]
    recommendations: List[str]

# Backend Output
class BackendOutput(BaseModel):
    api_endpoints: List[APIEndpoint]
    database_changes: List[DatabaseChange]
    implementation_notes: List[str]
```

## Coordination

Workers coordinate through:

- **EVENTS.jsonl**: Real-time coordination events
- **SESSION.md**: Session configuration and documentation
- **Protocol adherence**: Shared execution patterns

### Event Example (Schema-Compliant)

```json
{
  "timestamp": "2025-01-01T12:00:00Z",
  "type": "worker_spawned",
  "agent": "frontend-worker",
  "details": {
    "note": "startup complete"
  }
}
```

## Optimization

All agents optimized for:

- **Token efficiency**: Minimal verbose content
- **Fast startup**: Streamlined initialization
- **Clear focus**: Single responsibility principle
- **Production readiness**: No placeholder code
