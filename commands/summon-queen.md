---
name: summon-queen
description: Launch multi-agent orchestration via the Scribe and Queen agents.
arguments: $ARGUMENTS
---

# 👑 Hive-Mind Orchestration Workflow

This command initiates a new session by first using the `scribe-worker` to create the session, and then activating the `queen-orchestrator` to analyze the task and manage the workers.

## 🚨 WORKFLOW ENFORCEMENT

The `/summon-queen` command follows a strict, two-phase process. You must execute these steps in order.

### Phase 1: Session Creation via Pydantic AI Scribe

**Your first action is to ensure you're in the .claude directory, then run the Pydantic AI scribe to create the session.** This ensures reliable session creation with proper logging.

**MANDATORY BASH EXECUTION:**
First, navigate to the .claude directory, then use the `Bash` tool to run the Pydantic AI scribe with these exact parameters:

```bash
python agents/pydantic_ai/scribe/runner.py create --task "$ARGUMENTS" --model openai:gpt-5-mini
```

The Pydantic AI scribe will:

- Generate proper session ID in YYYY-MM-DD-HH-mm-shorttaskdescription format
- Create complete session directory structure (no .gitkeep files)
- Log `worker_spawned` and `session_created` events automatically
- Return JSON with `session_id`, `session_path`, and other metadata

Parse the JSON response to extract the `session_id` for the next phase.

### Phase 2: Orchestration via Pydantic AI Queen

**Once you have the `session_id` from the Scribe, your second action is to run the Pydantic AI Queen orchestrator to perform the strategic analysis.**

**MANDATORY BASH EXECUTION:**
From the .claude directory, use the `Bash` tool to run the Pydantic AI Queen orchestrator with these exact parameters:

```bash
python agents/pydantic_ai/queen/runner.py --session [session_id_from_scribe] --task "$ARGUMENTS" --model openai:o3-mini
```

## 👑 Explicit Queen Orchestrator Responsibilities

The Pydantic AI Queen is **THE CENTRAL ORCHESTRATOR** and MUST perform these critical functions in order:

### 🔍 Pre-Orchestration Analysis (MANDATORY)
**Before spawning any workers, the Queen MUST:**

1. **Protocol Compliance Self-Check**:
   - Read `.claude/agents/queen-orchestrator.md` for configuration
   - Load ALL required protocols from `.claude/protocols/` directory
   - Execute startup protocol checklist from `worker-startup-protocol.md`
   - Log protocol compliance verification to EVENTS.jsonl

2. **System Impact Analysis**:
   - Analyze task complexity and cross-service dependencies
   - Identify which SmartWalletFX services will be affected (API, Frontend, Sara, Crypto-Data, Archon)
   - Map domain boundaries and event flow requirements
   - Document architectural constraints in SESSION.json

3. **Context Loading Strategy**:
   - Determine task complexity level (1-4) based on cross-service impact
   - Load appropriate memory bank context using tag-based filtering
   - Access relevant protocol patterns from pattern library
   - Establish token efficiency baseline for worker coordination

### 🎯 Strategic Task Decomposition (MANDATORY)
**The Queen MUST intelligently break down tasks:**

1. **Domain Analysis**:
   - Map task requirements to service domains (User/Portfolio → API, UI → Frontend, etc.)
   - Identify cross-domain dependencies and coordination points
   - Assess research requirements vs implementation complexity

2. **Worker Assignment Strategy**:
   - Select optimal worker combination based on task complexity
   - Define worker priorities and blocking/dependency relationships
   - Create worker-specific prompts with domain context and protocols
   - Establish coordination checkpoints and escalation triggers

3. **Risk Assessment**:
   - Identify potential architectural violations or domain boundary breaches
   - Plan failure recovery strategies for critical path workers
   - Define success criteria and completion verification methods

### ⚙️ Orchestration Plan Generation (MANDATORY OUTPUT)
**The Queen MUST generate a comprehensive QueenOrchestrationPlan containing:**

1. **Worker Deployment Manifest**:
   - Exact worker types needed with justification
   - Worker spawn order and dependency chain
   - Protocol compliance requirements for each worker
   - Expected deliverables and coordination interfaces

2. **Session Coordination Framework**:
   - EVENTS.jsonl monitoring strategy with specific event types
   - Cross-worker communication patterns and escalation rules
   - Token efficiency targets and context loading optimization
   - Progress checkpoints and completion criteria

3. **Quality Assurance Strategy**:
   - Research verification requirements before implementation
   - Code quality standards and architectural compliance checks
   - Integration testing and cross-service validation points
   - Final synthesis and deliverable consolidation plan

### 📊 Active Coordination Oversight (CONTINUOUS)
**Throughout execution, the Queen MUST:**

1. **Real-time Monitoring**:
   - Continuously analyze EVENTS.jsonl for protocol violations
   - Monitor worker progress against established checkpoints
   - Detect blocking dependencies and coordinate resolution
   - Identify performance bottlenecks and optimization opportunities

2. **Protocol Enforcement**:
   - Verify all workers complete startup protocols before task work
   - Ensure research-first compliance for implementation tasks
   - Monitor event logging standards and coordination patterns
   - Intervene when protocol violations are detected

3. **Adaptive Coordination**:
   - Adjust worker priorities based on real-time progress
   - Resolve cross-worker conflicts and dependency issues
   - Optimize resource allocation and context sharing
   - Trigger escalation procedures for critical path failures

### 🎯 Completion & Synthesis (FINAL PHASE)
**Upon worker completion, the Queen MUST:**

1. **Results Validation**:
   - Verify all workers completed assigned tasks with proper protocols
   - Validate deliverables meet quality and architectural standards
   - Ensure cross-service integration points function correctly
   - Document any architectural decisions or pattern discoveries

2. **Synthesis Coordination**:
   - Trigger Pydantic AI scribe for final synthesis phase
   - Consolidate worker outputs into coherent deliverable
   - Update memory bank with architectural decisions and patterns
   - Log session completion with success metrics and lessons learned

**CRITICAL**: The Queen's orchestration plan must be **SPECIFIC AND ACTIONABLE** - no generic worker assignments. Each worker must receive detailed context, specific protocols, and clear success criteria.

**CRITICAL**: You must pass the exact `session_id` received from the Pydantic AI scribe to the Queen orchestrator.

### Phase 3: Automatic Claude Worker Deployment

**The Queen orchestrator now automatically spawns Claude Worker agents using the Task framework. This establishes the proper hierarchy: Queen → Claude Workers → Pydantic AI Workers.**

**Architecture Flow:**
1. **Queen Analysis Complete**: The Queen has generated the orchestration plan with worker assignments
2. **Automatic Claude Worker Spawning**: The Queen automatically spawns Claude Worker agents (.md files) using the Task tool
3. **Claude Worker Initialization**: Each Claude Worker agent loads its configuration, joins the session, and executes startup protocols
4. **Pydantic AI Worker Spawning**: Each Claude Worker agent then spawns its corresponding Pydantic AI worker
5. **Coordinated Execution**: Workers coordinate through the session event system

**Worker Hierarchy Mapping:**

- `analyzer-worker.md` → `pydantic_ai/analyzer/` - Security, performance, and code quality analysis
- `architect-worker.md` → `pydantic_ai/architect/` - System architecture and design analysis  
- `backend-worker.md` → `pydantic_ai/backend/` - API, database, and service implementation
- `devops-worker.md` → `pydantic_ai/devops/` - Infrastructure, deployment, and operations
- `researcher-worker.md` → `pydantic_ai/researcher/` - Industry standards and best practices research
- `frontend-worker.md` → `pydantic_ai/frontend/` - UI/UX and client-side implementation
- `designer-worker.md` → `pydantic_ai/designer/` - Design patterns and user experience
- `test-worker.md` → `pydantic_ai/test/` - Testing strategies and quality assurance

## 🛠️ Enhanced Protocol Implementation for Workers

**No Manual Worker Spawning Required:**
The Queen orchestrator handles all worker spawning automatically through the Task framework. Each Claude Worker agent receives detailed instructions including:

### 📋 Mandatory Worker Initialization Protocol

**EVERY spawned worker MUST execute this EXACT sequence before beginning task work:**

1. **Protocol Compliance Verification**:
   ```
   - Load worker configuration from `.claude/agents/[worker-type].md`
   - Read ALL protocols listed in the `protocols:` field
   - Execute startup checklist from `worker-startup-protocol.md`
   - Log protocol compliance to EVENTS.jsonl with timestamp
   ```

2. **Session Integration**:
   ```
   - Locate session directory: `Docs/hive-mind/sessions/{session_id}/`
   - Load session context from SESSION.json
   - Register worker spawn event in EVENTS.jsonl
   - Verify Queen orchestration plan alignment
   ```

3. **Context Loading & Domain Preparation**:
   ```
   - Load domain-specific memory bank context using tags
   - Access relevant architectural patterns from pattern library
   - Establish cross-service dependencies if applicable
   - Prepare research phase according to research-protocol.md
   ```

4. **Communication Channel Establishment**:
   ```
   - Initialize event logging with standardized format
   - Set up coordination checkpoints with other workers
   - Configure escalation triggers and blocking event handling
   - Validate Queen oversight communication channel
   ```

### 🔄 Continuous Protocol Adherence

**Throughout task execution, ALL workers MUST:**

1. **Research-First Enforcement**:
   - Document research findings before ANY implementation
   - Use Context7/Serena for technical research, Archon for architectural patterns
   - Log research completion event before proceeding to implementation
   - No code changes without documented research justification

2. **Event Stream Maintenance**:
   - Log significant operations with standardized event format
   - Report blocking dependencies immediately to coordination system
   - Update progress checkpoints as defined in orchestration plan  
   - Signal completion with deliverable summary and metrics

3. **Quality Assurance Compliance**:
   - Follow SOLID principles and architectural constraints
   - Verify domain boundaries are not violated
   - Test cross-service integration points where applicable
   - Document any architectural decisions or pattern discoveries

4. **Coordination & Escalation**:
   - Monitor EVENTS.jsonl for coordination requests from other workers
   - Respond to Queen oversight inquiries within defined timeframes
   - Escalate blocking issues that cannot be self-resolved
   - Participate in synthesis phase coordination as directed

### ⚠️ Protocol Violation Handling

**If protocol violations are detected:**

1. **Self-Correction Process**:
   - Immediately identify and log the protocol violation
   - Complete all missing protocol steps before continuing
   - Update EVENTS.jsonl with correction actions taken
   - Resume task execution only after full compliance restored

2. **Queen Intervention Triggers**:
   - Missing 2 consecutive event logging checkpoints
   - Research phase bypassed without documentation
   - Domain boundary violations detected
   - Cross-worker coordination failures

3. **Failure Recovery**:
   - Worker must log detailed error context to DEBUG.jsonl
   - Attempt graceful degradation if possible
   - Trigger escalation to Queen if critical path affected
   - Exit with non-zero status if unrecoverable failure

### 🎯 Worker-Specific Protocol Enhancements

**Each worker type has additional protocol requirements:**

- **Implementation Workers** (backend, frontend, devops): Enhanced research-protocol compliance
- **Analysis Workers** (analyzer, architect): Deep context loading and cross-service analysis
- **Research Workers** (researcher, designer): Pattern library contribution requirements
- **Quality Workers** (test): Integration testing and architectural validation protocols

## 📊 Advanced Monitoring & Coordination

### 🔍 Real-time Session Monitoring

**Queen Oversight Dashboard:**
```bash
# Monitor active session progress
tail -f Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl

# Check protocol compliance status
grep "protocol_compliance" Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl

# Monitor worker coordination health
grep "coordination\|blocking\|escalation" Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl

# Review session state and orchestration status
cat Docs/hive-mind/sessions/{session_id}/SESSION.json | jq '.orchestration_status'
```

**Critical Event Types to Monitor:**
- `worker_spawned` - Worker initialization events
- `protocol_compliance_verified` - Startup protocol completion
- `research_phase_complete` - Research-first enforcement compliance
- `coordination_request` - Cross-worker dependency requests
- `blocking_event` - Workers waiting on dependencies
- `escalation_triggered` - Issues requiring Queen intervention
- `worker_completed` - Task completion with metrics
- `protocol_violation` - Compliance failures requiring correction

### ⚡ Token Efficiency & Performance Metrics

**Session Performance Tracking:**
- **Context Loading Efficiency**: Track memory bank context hits/misses
- **Protocol Compliance Rate**: Measure startup protocol adherence (target: 100%)
- **Cross-Worker Coordination Speed**: Average time to resolve blocking events
- **Research Reuse Rate**: Pattern library usage vs new research generation
- **Token Optimization**: Actual vs projected token usage per complexity level

### 🎯 Success Criteria & Quality Gates

**Orchestration Success Metrics:**

1. **Protocol Adherence KPIs**:
   - 100% workers complete initialization protocols
   - 0% research phase bypasses without documentation
   - <10 minute average response time for coordination requests
   - <5% protocol violation rate requiring Queen intervention

2. **Delivery Quality Standards**:
   - All deliverables meet architectural constraints
   - Domain boundaries maintained with 0% violations
   - Cross-service integration points validated
   - Pattern library contributions documented

3. **Operational Efficiency Targets**:
   - 60-80% token usage reduction through optimized context loading
   - 40-60% faster coordination through standardized protocols
   - 90%+ session resumption success rate after interruptions
   - <15% duplicate research through pattern library reuse

### 🚨 Automated Quality Assurance

**Real-time Quality Checks:**
- Workers write progress events to `EVENTS.jsonl` with standardized format
- Workers create structured output files in `session_directory/workers/notes/`
- Cross-worker coordination handled via event system with automatic dependency tracking
- Failed workers log detailed error context to DEBUG.jsonl and exit with non-zero status
- Completed workers log completion events with deliverable metrics and quality indicators

**Quality Gate Enforcement:**
- Research phase verification before implementation begins
- Architectural compliance checks at coordination checkpoints  
- Cross-service integration validation for multi-domain tasks
- Protocol adherence verification throughout execution lifecycle

**Worker Output Structure:**

```
session_directory/
├── EVENTS.jsonl              # Worker progress and coordination events
├── DEBUG.jsonl               # Debug logs and error details
├── SESSION.json              # Session state and orchestration plan
└── workers/
    └── notes/
        ├── analyzer_output.json      # Structured analysis results
        ├── analyzer_notes.md         # Human-readable analysis
        ├── architect_output.json     # Architecture recommendations
        └── ...                       # Other worker outputs
```

---

## 🔄 Enhanced Orchestration Lifecycle

### Phase-by-Phase Execution with Protocol Enforcement

1. **🚀 Summon Initiation**
   - You, the top-level agent, receive the `/summon-queen` command
   - Navigate to `.claude` directory for Pydantic AI execution
   - Validate command arguments and task complexity assessment

2. **📝 Session Creation via Pydantic AI Scribe**
   - Execute Pydantic AI scribe with exact parameters for reliable session creation
   - Parse returned JSON to extract `session_id` and session metadata
   - Verify session directory structure creation and initial logging setup

3. **👑 Strategic Orchestration via Pydantic AI Queen**
   - Execute Pydantic AI Queen with session context for intelligent task analysis
   - **Queen MUST complete ALL mandatory responsibilities:**
     - Protocol compliance self-check and system impact analysis
     - Strategic task decomposition with domain mapping
     - Comprehensive orchestration plan generation
     - Quality assurance strategy definition
   - Verify QueenOrchestrationPlan generation with specific worker assignments

4. **🛠️ Automatic Worker Deployment with Enhanced Protocol Compliance**
   - Queen automatically spawns Claude Worker agents using Task framework
   - **EVERY worker MUST execute mandatory initialization protocol:**
     - Protocol compliance verification and session integration
     - Context loading and communication channel establishment
     - Research phase preparation and coordination setup
   - Establish proper hierarchy: Queen → Claude Workers → Pydantic AI Workers
   - Verify all workers complete startup protocols before task execution

5. **📊 Active Monitoring with Real-time Quality Assurance**
   - Workers coordinate through standardized event system with continuous protocol adherence
   - Queen maintains active oversight with real-time monitoring and protocol enforcement
   - Progress tracked via EVENTS.jsonl with specific event types and quality gates
   - Automatic escalation triggered for protocol violations or coordination failures

6. **🎯 Completion & Synthesis with Quality Validation**
   - Workers signal completion with deliverable summaries and success metrics
   - Queen validates all deliverables meet architectural and quality standards
   - Execute Pydantic AI scribe synthesis phase with consolidated worker outputs
   - Update memory bank with architectural decisions and learned patterns

### 🎪 Your Role as Orchestration Initiator

**Your responsibilities are to:**
- **Initiate the two-phase process correctly** (Scribe → Queen) with exact parameter passing
- **Ensure protocol enforcement** by verifying Queen executes all mandatory responsibilities
- **Monitor session health** through the established oversight dashboard commands
- **Verify quality gates** are met at each phase transition
- **Maintain architectural compliance** throughout the orchestration lifecycle

**Critical Success Factors:**
- Session ID continuity between Scribe and Queen phases
- Protocol compliance verification at each major phase
- Quality gate enforcement before phase transitions  
- Architectural constraint maintenance throughout execution

Your role is to initiate and oversee this comprehensive orchestration process, ensuring protocol adherence and quality standards are maintained throughout the entire lifecycle.
