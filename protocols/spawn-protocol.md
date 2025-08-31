# Spawn Protocol
## Worker Selection and Deployment Guidelines

---

## Core Principles

1. **Task Coverage**: Ensure complete domain coverage for all complexity levels
2. **Service Awareness**: Match workers to target service domains
3. **Token Efficiency**: Balance comprehensive analysis with resource usage
4. **Pattern Recognition**: Apply proven worker combinations

---

## Service Domain Mapping

### Service Detection Rules

| Service | Keywords | Required Workers |
|---------|----------|------------------|
| **crypto-data** | crypto, market, trading, websocket, real-time | backend-worker, analyzer-worker, devops-worker |
| **api** | api, endpoint, rest, graphql, backend | backend-worker, architect-worker |
| **frontend** | ui, ux, react, component, user interface | frontend-worker, designer-worker |
| **sara** | context, intelligence, memory, ai, embedding | backend-worker, analyzer-worker |
| **full-stack** | full, entire, comprehensive, all services | architect-worker, backend-worker, frontend-worker, devops-worker |

---

## Worker Selection Algorithm

### Step 1: Complexity-Based Minimums

| Complexity | Minimum Workers | Base Configuration |
|------------|----------------|--------------------|
| Level 1 | 1-2 | analyzer-worker |
| Level 2 | 2-3 | analyzer-worker, backend-worker |
| Level 3 | 4-5 | architect-worker, backend-worker, analyzer-worker, devops-worker |
| Level 4 | 5+ | architect-worker, backend-worker, frontend-worker, analyzer-worker, devops-worker |

### Step 2: Domain Coverage Requirements

```python
def calculate_domain_coverage(workers, task_focus):
    """
    Ensure critical domains are covered based on task focus
    """
    coverage_map = {
        'security': ['analyzer-worker', 'backend-worker', 'devops-worker'],
        'performance': ['analyzer-worker', 'backend-worker', 'devops-worker'],
        'scalability': ['architect-worker', 'devops-worker', 'backend-worker'],
        'architecture': ['architect-worker', 'analyzer-worker', 'backend-worker'],
        'implementation': ['backend-worker', 'frontend-worker', 'test-worker']
    }
    
    required_workers = set()
    for domain in task_focus:
        if domain in coverage_map:
            required_workers.update(coverage_map[domain])
    
    return list(required_workers)
```

### Step 3: Task Pattern Matching

| Pattern | Indicators | Worker Configuration |
|---------|------------|----------------------|
| **Architecture Analysis** | architecture, analyze, comprehensive | architect-worker, backend-worker, analyzer-worker, devops-worker, test-worker |
| **Security Audit** | security, audit, vulnerability | analyzer-worker, backend-worker, devops-worker |
| **Performance Optimization** | performance, optimize, bottleneck | analyzer-worker, backend-worker, devops-worker |
| **Feature Implementation** | implement, feature, add, create | backend-worker, test-worker, frontend-worker* |
| **Bug Fix** | fix, bug, issue, problem | analyzer-worker, backend-worker* |

*Optional based on specific context

---

## Spawn Validation Checklist

### Pre-Spawn Validation

```python
def validate_spawn_decision(workers, task, complexity):
    """
    Validate worker selection before spawning
    """
    checks = [
        # Minimum worker count met
        len(workers) >= get_minimum_workers(complexity),
        
        # Architecture tasks have architect
        not ('architecture' in task.lower()) or ('architect-worker' in workers),
        
        # Backend tasks have backend worker
        not ('backend' in task.lower()) or ('backend-worker' in workers),
        
        # Implementation has test coverage
        not (any(w in workers for w in ['backend-worker', 'frontend-worker'])) or ('test-worker' in workers),
        
        # Infrastructure review for scalability
        not ('scalability' in task.lower()) or ('devops-worker' in workers)
    ]
    
    return all(checks)
```

### Post-Spawn Monitoring

- **Coverage Score**: Track domain coverage percentage
- **Worker Utilization**: Monitor active participation
- **Task Completion**: Verify all subtasks are addressed
- **Quality Metrics**: Measure output quality and completeness

---

## Queen Integration

### Worker Planning Method

```python
def plan_workers(task_description, complexity_level):
    """
    Queen's worker planning implementation
    """
    # 1. Detect target service
    service = detect_service(task_description)
    
    # 2. Get base workers for complexity
    workers = get_complexity_base_workers(complexity_level)
    
    # 3. Add service-specific workers
    workers.extend(get_service_workers(service))
    
    # 4. Match task patterns
    pattern = match_task_pattern(task_description)
    if pattern:
        workers.extend(pattern['required_workers'])
    
    # 5. Ensure domain coverage
    focus_areas = extract_focus_areas(task_description)
    workers.extend(calculate_domain_coverage(workers, focus_areas))
    
    # 6. Deduplicate and validate
    workers = list(set(workers))
    if not validate_spawn_decision(workers, task_description, complexity_level):
        workers = apply_corrections(workers, task_description, complexity_level)
    
    return workers
```

---

## Continuous Improvement

### Success Pattern Recording

```json
{
  "session_id": "2024-08-30-14-45-crypto-scalability-analysis",
  "workers_used": ["architect-worker", "backend-worker", "analyzer-worker", "devops-worker"],
  "task_type": "scalability_analysis",
  "coverage_achieved": 95,
  "quality_score": 92,
  "lessons_learned": [
    "Devops-worker critical for infrastructure insights",
    "Architect-worker provided valuable system-wide perspective"
  ]
}
```

### Pattern Library Updates

- Record successful worker combinations
- Note domain blind spots discovered
- Update service detection keywords
- Refine coverage requirements

---

## Quick Reference

### Decision Matrix

| If Task Contains | Must Include | Should Include | Consider |
|-----------------|--------------|----------------|----------|
| "architecture" | architect-worker | analyzer-worker | backend-worker |
| "security" | analyzer-worker | backend-worker, devops-worker | test-worker |
| "performance" | analyzer-worker | backend-worker, devops-worker | architect-worker |
| "implement" | backend-worker | test-worker | frontend-worker |
| "scalability" | devops-worker | architect-worker | backend-worker |
| "bug" or "fix" | analyzer-worker | backend-worker | test-worker |

### Complexity Guidelines

- **Level 1**: Simple, focused tasks - minimal workers
- **Level 2**: Multi-aspect tasks - balanced coverage
- **Level 3**: Complex analysis - comprehensive team
- **Level 4**: System-wide changes - full coverage

---

## 🔧 Implementation Requirements

### Session ID Format
**MANDATORY**: All sessions must use format: `YYYY-MM-DD-HH-mm-shorttaskdescription`

```python
# CORRECT: 2025-08-31-14-25-crypto-architecture-analysis
# WRONG: crypto-data-architecture-analysis_20250831_142500
```

### Event Logging Rules
1. **Queen MUST log `queen_spawned` as first action**
2. **Workers log their OWN `worker_spawned` events** (not the Queen)
3. **Queen logs `tasks_assigned`** for context preparation
4. **Scribe logs `worker_spawned` when activated for synthesis**

### File Creation Rules
- **NO .gitkeep files** in session directories
- Only create necessary session files: STATE.json, EVENTS.jsonl, etc.

### Spawn Reality
In Claude Code, "spawning" means:
- **Context Preparation**: Queen creates worker configs in STATE.json
- **Task Assignment**: Queen logs `tasks_assigned` events
- **Worker Activation**: Workers log `worker_spawned` when they actually start
- **State Updates**: Workers update their status to `in_progress`

---

## Summary

This spawn protocol ensures:

1. **Complete Coverage**: No domain blind spots
2. **Efficient Selection**: Right workers for the task
3. **Validated Decisions**: Pre-spawn validation prevents gaps
4. **Continuous Learning**: Pattern library improves over time
5. **Token Optimization**: Balanced resource usage
6. **Proper Implementation**: Correct session IDs, event logging, and file creation