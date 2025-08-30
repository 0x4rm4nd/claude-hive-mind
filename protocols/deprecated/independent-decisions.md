# Independent Decision Reporting Protocol

## Overview
Workers can make independent technical decisions but MUST document and justify them for hive-mind coordination and learning.

## Decision Documentation Structure

### File Location
`Docs/hive-mind/sessions/{session-id}/workers/decisions/{worker-type}-decisions.md`

Examples:
- `backend-decisions.md`
- `frontend-decisions.md` 
- `test-decisions.md`
- `devops-decisions.md`

### Decision Template

```markdown
# {Worker-Type} Independent Decisions - Session {session-id}

## Decision Log

### Decision #{number} - {timestamp}
**Decision**: {Brief title of decision made}
**Context**: {What situation required this decision}
**Options Considered**: 
- Option A: {description} - {pros/cons}
- Option B: {description} - {pros/cons}
- Option C: {description} - {pros/cons}

**Selected**: Option B - {chosen option}

**Rationale**: {Why this option was chosen}
- Technical reasoning
- Time constraints
- Resource limitations
- Risk assessment
- SmartWalletFX integration considerations

**Impact**: {How this affects the project}
- Immediate effects
- Long-term implications
- Dependencies created/resolved

**Validation**: {How to verify this was correct}
- Tests to run
- Metrics to check
- Feedback to collect

**Reversibility**: {Can this be changed later?}
- Easy to reverse: Yes/No
- Cost of reversal: Low/Medium/High
- Timeline for reversal: X hours/days

---
```

## Notification Protocol

### 1. Document Decision
Write decision in worker's decisions file using template above.

### 2. Notify Hive-Mind via Unified Events Log
Add to EVENTS.jsonl (single unified log):

```jsonl
{"timestamp": "2025-01-15T14:40:00Z", "type": "decision", "event": "independent_decision", "agent": "backend-worker", "target": "all", "data": {"decision_id": "backend-001", "title": "JWT library selection", "message": "Chose Express-jwt over custom JWT implementation", "justification_file": "workers/decisions/backend-decisions.md", "impact": "medium", "reversible": true}}
```

### 3. Update State
If decision affects session state, update STATE.json metrics:
```json
{
  "session_metrics": {
    "decisions_made": 8,
    "pending_validations": 2,
    "...": "..."
  }
}
```

## Decision Categories

### Technical Architecture
- Library/framework selection
- Design pattern choices
- Database schema decisions
- API design choices

### Implementation Details
- Code structure decisions
- Error handling approaches
- Performance optimizations
- Security implementations

### Process Decisions
- Testing strategies
- Deployment approaches
- Code review processes
- Documentation formats

## Escalation Triggers

### Mandatory Queen Consultation
- Decisions affecting multiple workers
- Breaking changes to agreed interfaces
- Security-critical decisions
- Major architectural changes

### How to Escalate
1. Document decision in decisions file
2. Mark as "ESCALATION_REQUIRED" in title
3. Notify Queen via EVENTS.jsonl with type="notification" and event="escalation_required"
4. Wait for Queen coordination before proceeding

Example:
```markdown
### Decision #5 - ESCALATION_REQUIRED - 2025-01-15T14:40:00Z
**Decision**: Change authentication from JWT to OAuth2
**Context**: JWT doesn't meet new security requirements...
```

## Quality Assurance

### Decision Review Process
1. Self-review using template checklist
2. Impact assessment on other workers
3. Reversibility analysis
4. Future maintainability considerations

### Learning Integration
- Successful decisions → Pattern Library
- Failed decisions → Lessons Learned
- Complex decisions → Architecture Documentation

## Integration with Archon Tasks

### Link Decisions to Tasks
When making decisions that affect Archon tasks:

1. Update Archon task description with decision summary:
```
archon:manage_task(
  action="update",
  task_id="task-uuid",
  update_fields={
    "description": "Original description\n\nDECISION UPDATE: Chose Express-jwt library based on security analysis (see session decisions file)"
  }
)
```

2. Reference decision in task notes for traceability

### Decision-Driven Task Creation
Independent decisions may create new tasks:
- Update BACKLOG.jsonl with new tasks
- Create corresponding Archon tasks
- Link decision rationale in task description

## Examples

### Good Decision Documentation
```markdown
### Decision #3 - 2025-01-15T14:40:00Z
**Decision**: Use Prisma ORM instead of raw SQL
**Context**: Need to implement user authentication database layer quickly
**Options Considered**:
- Raw SQL: Full control, performance - Complex, time-consuming
- Prisma: Type safety, rapid development - Less control, learning curve
- TypeORM: Familiar patterns - Known performance issues

**Selected**: Prisma ORM

**Rationale**: 
- Type safety reduces authentication bugs (critical for financial app)
- Rapid development matches sprint timeline
- Team has Prisma experience from other services
- Performance adequate for auth workload (tested)

**Impact**: 
- Faster auth implementation (2 days saved)
- Consistent with user-service architecture
- Creates dependency on Prisma schema management

**Validation**: 
- Load test auth endpoints (target: <100ms response)
- Security audit SQL injection resistance
- Monitor memory usage in production

**Reversibility**: 
- Cost: Medium (2-3 days to rewrite)
- Timeline: Sprint 3 if needed
- Transition path: Export schema, rewrite queries
```

### Poor Decision Documentation
```markdown
### Decision #1
**Decision**: Used React hooks
**Rationale**: They're better
**Impact**: Code works
```

## Decision Metrics

Track decision quality in session metrics:
- Decision count per worker
- Escalation rate
- Reversal rate
- Implementation success rate

This helps improve hive-mind coordination over time.