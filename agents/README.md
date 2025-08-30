# Agent Configurations

Production-ready agent definitions for the hive-mind orchestration system.

## Agent Types

### Orchestrator
- **queen-orchestrator.md**: Master coordinator that plans and synthesizes

### Workers (8 Specialists)
- **researcher-worker.md**: Context7 research and best practices
- **architect-worker.md**: System design and architecture patterns
- **backend-worker.md**: API and database implementation
- **frontend-worker.md**: UI components and client-side logic
- **designer-worker.md**: UX/UI design and accessibility
- **test-worker.md**: Testing strategy and quality assurance
- **devops-worker.md**: Infrastructure and deployment
- **analyzer-worker.md**: Security and performance analysis

## Configuration Structure

Each agent file contains:

```yaml
---
name: agent-name
type: specialization
color: hex-color
description: brief description
capabilities: [list of capabilities]
priority: critical|high|medium|low
---
```

## Worker Standards

All workers follow:

1. **Mandatory Startup Protocol** (`.claude/protocols/startup_protocol_instructions.md`)
2. **Standardized Output Format** (JSON response + markdown notes)
3. **Coordination Patterns** (blocking/unblocking events)
4. **Research Integration** (Context7 for complexity >= 2)

## Output Requirements

### JSON Response
```json
{
  "worker": "worker-type",
  "status": "completed",
  "summary": {...},
  "findings": [...],
  "recommendations": [...]
}
```

### Notes File
```markdown
# [Worker Type] Analysis
## Executive Summary
## Detailed Findings
## Recommendations
## Evidence
```

## Coordination

Workers coordinate through:
- **EVENTS.jsonl**: Real-time coordination events
- **STATE.json**: Session configuration and status
- **Protocol adherence**: Shared execution patterns

## Optimization

All agents optimized for:
- **Token efficiency**: Minimal verbose content
- **Fast startup**: Streamlined initialization
- **Clear focus**: Single responsibility principle
- **Production readiness**: No placeholder code
