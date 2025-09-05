# Pydantic AI Agents Framework

> **Framework-enforced AI agents with guaranteed output validation and protocol compliance**

## 🏗️ Architecture Overview

This directory implements a **framework-enforced agent ecosystem** using Pydantic AI, providing structured, validated, and reliable AI agent behavior through code rather than instructions.

### **Core Philosophy: Framework-Enforced vs Instruction-Dependent**

| Aspect                  | Traditional Claude Code Agents              | Pydantic AI Agents                    |
| ----------------------- | ------------------------------------------- | ------------------------------------- |
| **Behavior Control**    | 📝 Markdown instructions (hope they follow) | 🏗️ Python code (impossible to ignore) |
| **Output Validation**   | ❌ Can return anything                      | ✅ Pydantic schema enforced           |
| **Protocol Compliance** | ❌ Manual, error-prone                      | ✅ Built into execution flow          |
| **Reliability**         | 🎲 Probabilistic                            | 🔒 Deterministic                      |
| **Debugging**           | 😵‍💫 "Why didn't it follow instructions?"     | 🔍 Python stack traces                |

---

## 📁 Directory Structure

```
agents/pydantic_ai/
├── README.md                    # This file - architecture documentation
├── __init__.py                  # Main package exports
├── cli.py                       # Unified CLI entry point
├── shared/                      # Common components
│   ├── __init__.py
│   ├── base_worker.py          # BaseWorker framework
│   ├── base_agent.py           # BaseAgentConfig pattern
│   ├── models.py               # Base models used across agents
│   ├── worker_config.py        # Worker configuration models
│   └── tools.py                # Shared utilities
├── queen/                       # 👑 Queen Orchestrator Agent
│   ├── __init__.py
│   ├── agent.py                # Pydantic AI agent + tools
│   ├── runner.py               # BaseWorker implementation
│   └── models.py               # Queen-specific schemas
├── scribe/                      # 📝 Scribe Agent
│   ├── __init__.py
│   ├── agent.py                # Pydantic AI agent
│   ├── runner.py               # BaseWorker implementation
│   └── models.py               # Scribe-specific schemas
└── [worker]/                    # 🔧 Specialist Workers
    ├── __init__.py
    ├── agent.py                # BaseAgentConfig pattern
    ├── runner.py               # BaseWorker implementation
    └── models.py               # Worker-specific schemas
```

### **Scalability Design**

This structure is designed for **easy expansion**. Adding a new agent is straightforward:

```
└── analyzer/                    # 🔍 New Agent Example
    ├── __init__.py
    ├── agent.py                # Pydantic AI agent definition
    ├── runner.py               # Execution logic
    ├── models.py               # Agent-specific schemas
    └── tools.py                # Agent-specific tools
```

---

## 🤖 Agent Roles & Responsibilities

### 👑 **Queen Orchestrator** (`queen/`)

**Role**: Master task coordinator and continuous workflow monitor

**Key Features**:

- **Intelligent Planning**: AI-powered worker selection and task decomposition
- **Continuous Monitoring**: Real-time worker progress tracking (30s intervals)
- **Framework-Enforced Outputs**: `QueenOrchestrationPlan` schema validation
- **Codebase Exploration**: Built-in tools for project analysis

**Core Responsibilities**:

1. **Strategic Analysis**: Deep task analysis to understand requirements
2. **Worker Selection**: Match tasks to optimal worker expertise
3. **Risk Assessment**: Identify blockers, dependencies, mitigation strategies
4. **Continuous Monitoring**: Track worker evolution, detect blocks/failures
5. **Quality Orchestration**: Ensure proper coordination and quality gates

**Usage**:

```bash
# Basic orchestration
python cli.py queen --session SESSION_ID --task "Analyze application security"

# With continuous monitoring
python cli.py queen --session SESSION_ID --task "..."  
```

**Schema Output**:

```python
class QueenOrchestrationPlan(BaseModel):
    complexity_assessment: int  # 1-4 complexity rating
    worker_assignments: List[WorkerAssignment]  # Required workers
    execution_strategy: Literal["parallel", "sequential", "hybrid"]
    coordination_notes: List[str]  # Important considerations
    identified_risks: List[str]   # Potential blockers
    mitigation_strategies: List[str]  # Risk mitigation
    # ... additional validated fields
```

### 📝 **Scribe Agent** (`scribe/`)

**Role**: Session lifecycle management and knowledge synthesis

**Key Features**:

- **Smart Session Creation**: AI-generated session IDs with task analysis
- **Complexity Assessment**: Automatic 1-4 complexity rating
- **Synthesis Generation**: Consolidate worker outputs into final reports
- **Protocol Integration**: Built-in event logging and state management

**Core Responsibilities**:

1. **Session Creation**: Generate structured session directories
2. **Task Summarization**: AI-powered session ID generation
3. **Knowledge Synthesis**: Combine worker outputs into comprehensive reports
4. **Event Logging**: Protocol-compliant activity tracking

**Usage**:

```bash
# Create new session
python cli.py scribe create --task "Comprehensive security audit of application services"

# Generate synthesis from completed workers
python cli.py scribe synthesis --session 2024-01-15-14-30-application-security-audit
```

**Schema Outputs**:

```python
class ScribeSessionCreationOutput(BaseModel):
    session_id: str           # AI-generated session identifier
    complexity_level: int     # 1-4 assessed complexity
    session_path: str         # Full directory path
    # ... additional validated fields

class TaskSummaryOutput(BaseModel):
    short_description: str    # 2-4 hyphenated words
    complexity_level: int     # 1-4 complexity assessment
    focus_areas: List[str]    # Main task focus areas
```

---

## 🚀 Usage Examples

### **Complete Workflow Example**

```bash
# 1. Create session with AI-powered session ID
python cli.py scribe create --task "Analyze application architecture focusing on security, performance, and scalability"
# Output: session_id: "2024-01-15-14-30-architecture-security-analysis"

# 2. Run Queen orchestrator with monitoring
python cli.py queen --session 2024-01-15-14-30-architecture-security-analysis --task "..." 

# 3. Queen monitors workers continuously (every 30s)
# ✅ Workers spawn and complete their analysis
# 🔍 Queen tracks: analysis_started, progress_update, worker_completed

# 4. Generate final synthesis
python cli.py scribe synthesis --session 2024-01-15-14-30-architecture-security-analysis
```

### **Advanced Queen Monitoring**

```bash
# Custom monitoring interval (every 60 seconds)
python cli.py queen --session SESSION_ID --task "..."  

# The Queen will:
# ✅ Log "monitoring_started" event
# 🔄 Check worker status every 60s
# 📊 Log "monitoring_heartbeat" with progress updates
# ⚠️  Detect blocked workers and log "workers_blocked_detected"
# ✅ Log "all_workers_completed" when finished
```

---

## 🔧 Technical Implementation

### **Framework Enforcement Benefits**

1. **Schema Validation**: Impossible to return malformed output

```python
# This CANNOT happen with Pydantic AI agents:
# ❌ Queen returns: "I think we should use analyzer and architect workers"
# ✅ Queen returns: QueenOrchestrationPlan(worker_assignments=[...], complexity_assessment=3)
```

2. **Built-in Protocol Compliance**:

```python
# Automatic event logging built into execution flow
log_event(session_id, "queen_spawned", worker, {...})  # Cannot be skipped
log_event(session_id, "orchestration_completed", worker, {...})  # Guaranteed
```

3. **Integrated Monitoring**:

```python
# Real-time worker monitoring loop
async def monitor_worker_progress(session_id, worker_assignments, interval=30):
    while not all_workers_complete:
        # Check EVENTS.jsonl for worker status
        # Detect blocked/failed workers
        # Log periodic heartbeats
        await asyncio.sleep(interval)
```

### **Agent Extension Pattern**

To add a new agent (e.g., `analyzer`):

1. **Create Directory Structure**:

```bash
mkdir -p agents/pydantic/analyzer
```

2. **Define Agent** (`analyzer/agent.py`):

```python
from pydantic_ai import Agent
from .models import AnalyzerOutput

analyzer_agent = Agent(
    model="google-gla:gemini-2.5-flash",
    output_type=AnalyzerOutput,  # Schema-enforced output
    system_prompt="You are a security and performance analyzer..."
)
```

3. **Create Runner** (`analyzer/runner.py`):

```python
def main():
    # CLI argument parsing
    # Run agent with validation
    # Output structured results
```

4. **Add to CLI** (`cli.py`):

```python
# Add analyzer subparser
analyzer_parser = subparsers.add_parser('analyzer')
# Route to analyzer runner
```

---

## 🎯 Key Advantages

### **1. Reliability Through Code**

- **No missed steps**: Framework enforces behavior
- **Consistent outputs**: Pydantic validation guarantees
- **Predictable debugging**: Python stack traces vs "AI didn't follow instructions"

### **2. Scalable Architecture**

- **Self-contained agents**: Each agent in its own directory
- **Clean separation**: Models, tools, and execution logic separated
- **Easy expansion**: Add new agents without touching existing ones

### **3. Intelligent Coordination**

- **Queen's continuous monitoring**: Real-time worker progress tracking
- **Automatic escalation**: Built-in detection of blocked/failed workers
- **Event-driven**: Protocol-compliant logging throughout execution

### **4. Developer Experience**

- **Single CLI**: `python cli.py [agent] [options]`
- **Type safety**: Full Pydantic validation and IDE support
- **Framework integration**: Built-in protocol and session management

---

## 🔄 Migration from Instruction-Based Agents

**Before** (Traditional markdown-based agents):

- 500+ lines of markdown instructions per agent
- Manual protocol compliance (error-prone)
- Unstructured output (can return anything)
- Hope-based behavior ("please remember to...")
- Inconsistent execution patterns across agents

**After** (Framework-enforced Pydantic AI agents):

- Code-enforced behavior (impossible to ignore)
- Automatic protocol compliance (built-in)
- Schema-validated output (`WorkerOutput` subclasses)
- Framework-guaranteed behavior ("cannot skip steps")
- 100% consistent BaseWorker pattern across all agents

This represents the evolution from **instruction-dependent AI** to **framework-enforced AI** - moving from hoping agents follow instructions to making compliance structurally impossible to avoid.

---

## 🎯 **Max Subscription Integration**

All agents automatically support **zero-cost operation** via Claude Code's Max subscription through custom model names:

```python
# Standard usage - routes through Claude Code Max subscription
from pydantic_ai import Agent

agent = Agent('custom:max-subscription')      # Default: Sonnet 4
agent = Agent('custom:claude-opus-4')         # Opus 4 model
agent = Agent('custom:claude-sonnet-4')       # Sonnet 4 model
agent = Agent('custom:claude-3-7-sonnet')     # Sonnet 3.7 model
```

**Key Benefits**:
- ✅ **Zero API costs** - Uses Claude Code subscription instead of direct API calls
- ✅ **Automatic activation** - Works immediately after importing shared module
- ✅ **Seamless integration** - Drop-in replacement for standard model names
- ✅ **Full model support** - Access to latest Claude models via Max subscription

**Implementation**: The `MaxSubscriptionProvider` automatically intercepts `custom:*` model requests and routes them through Claude Code's task execution system with proper model mapping and response formatting.

---

## 🔧 **Worker Agents** (Specialized Implementation Agents)

### 🔍 **Analyzer Worker** (`analyzer/`)

**Role**: Security analysis, performance optimization, and code quality assessment
**Core Capabilities**:

- **Security Analysis**: OWASP Top 10, vulnerability assessment, authentication/authorization review
- **Performance Profiling**: Bottleneck identification, N+1 queries, algorithm optimization
- **Code Quality**: Complexity metrics, test coverage, technical debt analysis
- **Dependency Analysis**: Package vulnerabilities, license compliance, supply chain risks

**Usage**:

```bash
python cli.py analyzer --session SESSION_ID --task "Security and performance analysis"
```

### 🏗️ **Architect Worker** (`architect/`)

**Role**: System design, scalability patterns, and technical architecture
**Core Capabilities**:

- **System Architecture**: Microservices, monoliths, serverless, hybrid patterns
- **Scalability Design**: Horizontal/vertical scaling, caching, distributed systems
- **Design Patterns**: SOLID principles, DDD, CQRS, event sourcing
- **Technology Evaluation**: Framework selection, database choices, integration patterns

**Usage**:

```bash
python cli.py architect --session SESSION_ID --task "Architecture review and recommendations"
```

### ⚙️ **Backend Worker** (`backend/`)

**Role**: API development, database design, and service implementation
**Core Capabilities**:

- **API Development**: RESTful services, GraphQL, authentication, authorization
- **Database Design**: Schema modeling, query optimization, migrations, performance
- **Service Architecture**: Business logic, transaction management, integration patterns
- **Security Implementation**: JWT, OAuth2, data protection, input validation

**Usage**:

```bash
python cli.py backend --session SESSION_ID --task "API implementation and database optimization"
```

### 🎨 **Designer Worker** (`designer/`)

**Role**: User experience design, visual design, and accessibility
**Core Capabilities**:

- **UX Design**: User journey mapping, information architecture, usability optimization
- **Visual Design**: Brand consistency, typography, color systems, layout design
- **Accessibility**: WCAG compliance, inclusive design, assistive technology support
- **Design Systems**: Component libraries, design tokens, pattern documentation

**Usage**:

```bash
python cli.py designer --session SESSION_ID --task "UX/UI design review and accessibility audit"
```

### 🚀 **DevOps Worker** (`devops/`)

**Role**: Infrastructure, deployment, monitoring, and CI/CD pipelines
**Core Capabilities**:

- **Infrastructure Management**: Container orchestration, cloud platforms, IaC
- **CI/CD Pipelines**: Automated deployment, quality gates, rollback strategies
- **Monitoring**: Metrics collection, alerting, observability, performance tracking
- **Security Operations**: DevSecOps, compliance automation, access control

**Usage**:

```bash
python cli.py devops --session SESSION_ID --task "Infrastructure optimization and monitoring setup"
```

### 💻 **Frontend Worker** (`frontend/`)

**Role**: UI/UX implementation, component architecture, and state management
**Core Capabilities**:

- **Component Architecture**: Modern frameworks, reusable components, performance optimization
- **State Management**: Redux, Context API, async state, data flow patterns
- **UI Implementation**: Responsive design, accessibility, cross-browser compatibility
- **Performance Optimization**: Bundle optimization, lazy loading, rendering efficiency

**Usage**:

```bash
python cli.py frontend --session SESSION_ID --task "Component implementation and state management"
```

### 🔬 **Researcher Worker** (`researcher/`)

**Role**: Technical research, best practices, and industry standards analysis
**Core Capabilities**:

- **Technology Evaluation**: Framework comparisons, tool assessment, technology trends
- **Best Practices Research**: Industry standards, compliance frameworks, methodologies
- **Competitive Analysis**: Market intelligence, technology landscape, adoption patterns
- **Evidence-Based Insights**: Credible sources, research validation, actionable recommendations

**Usage**:

```bash
python cli.py researcher --session SESSION_ID --task "Technology evaluation and best practices research"
```

### 🧪 **Test Worker** (`test/`)

**Role**: Testing strategy, quality assurance, and test coverage analysis
**Core Capabilities**:

- **Test Strategy**: Test pyramid, automation strategy, quality gates
- **Test Implementation**: Unit, integration, e2e, performance, security testing
- **Quality Assurance**: Coverage analysis, defect prevention, test reliability
- **Testing Infrastructure**: CI/CD integration, test environments, reporting

**Usage**:

```bash
python cli.py test --session SESSION_ID --task "Comprehensive testing strategy and implementation"
```

---

**Ready for production**: Framework-enforced reliability, scalable architecture, and intelligent coordination. 🚀
