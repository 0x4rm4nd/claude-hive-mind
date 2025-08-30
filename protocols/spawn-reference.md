# Spawn Reference
## Quick Decision Guide for Queen Orchestrator

---

## Worker Selection Decision Tree

```
START → Analyze Task Description
         ↓
    [Complexity Level?]
         ↓
    ┌────┴────┬────┴────┬────┴────┐
    1         2         3         4
    ↓         ↓         ↓         ↓
  1-2       2-3       4-5       5+
 workers   workers   workers   workers
    ↓         ↓         ↓         ↓
 [Service     [Domain    [Full     [System
  Specific]   Coverage]  Team]     Wide]
```

---

## Instant Worker Selection

### By Task Type

| Task Keyword | Instant Workers |
|--------------|----------------|
| "fix bug" | analyzer-worker, backend-worker |
| "implement feature" | backend-worker, test-worker, frontend-worker |
| "analyze architecture" | architect-worker, backend-worker, analyzer-worker, devops-worker |
| "optimize performance" | analyzer-worker, backend-worker, devops-worker |
| "security audit" | analyzer-worker, backend-worker, devops-worker |
| "scalability review" | architect-worker, devops-worker, backend-worker |

### By Service Target

| Service | Core Workers |
|---------|-------------|
| crypto-data | backend-worker, analyzer-worker, devops-worker |
| api | backend-worker, architect-worker |
| frontend | frontend-worker, designer-worker |
| sara | backend-worker, analyzer-worker |
| full-stack | architect-worker, backend-worker, frontend-worker, devops-worker |

---

## Complexity Quick Guide

### Level 1 - Simple Tasks
- **Workers**: 1-2
- **Base**: analyzer-worker
- **Examples**: Bug fixes, simple queries, documentation

### Level 2 - Standard Tasks
- **Workers**: 2-3
- **Base**: analyzer-worker, backend-worker
- **Examples**: Feature implementation, API changes, UI updates

### Level 3 - Complex Tasks
- **Workers**: 4-5
- **Base**: architect-worker, backend-worker, analyzer-worker, devops-worker
- **Examples**: Architecture analysis, performance optimization, security audits

### Level 4 - System-Wide Tasks
- **Workers**: 5+
- **Base**: Full team deployment
- **Examples**: Major refactoring, system redesign, comprehensive audits

---

## Validation Checklist

✓ Minimum workers for complexity level?
✓ Domain expertise covered?
✓ Service-specific workers included?
✓ Test coverage for implementation?
✓ Infrastructure review for scalability?

---

## Common Patterns

### Pattern 1: Implementation
```
backend-worker (required)
test-worker (required)
frontend-worker (if UI involved)
architect-worker (if design decisions)
```

### Pattern 2: Analysis
```
analyzer-worker (required)
architect-worker (for system-wide)
backend-worker (for implementation details)
devops-worker (for infrastructure)
```

### Pattern 3: Optimization
```
analyzer-worker (required)
backend-worker (required)
devops-worker (required)
architect-worker (if architectural changes)
```

---

## Red Flags - Add More Workers

⚠️ "Architecture" without architect-worker
⚠️ "Security" without analyzer-worker
⚠️ "Scalability" without devops-worker
⚠️ Implementation without test-worker
⚠️ Less than minimum for complexity level

---

## Example Spawn Commands

### Bug Fix (Level 1)
```python
workers = ["analyzer-worker", "backend-worker"]
```

### Feature Implementation (Level 2)
```python
workers = ["backend-worker", "test-worker", "frontend-worker"]
```

### Architecture Analysis (Level 3)
```python
workers = ["architect-worker", "backend-worker", "analyzer-worker", "devops-worker", "test-worker"]
```

### System Redesign (Level 4)
```python
workers = ["architect-worker", "backend-worker", "frontend-worker", "analyzer-worker", "devops-worker", "test-worker", "designer-worker"]
```

---

## Summary Formula

**Workers = Base(Complexity) + Service(Domain) + Pattern(Task) - Duplicates**

Always validate before spawning!