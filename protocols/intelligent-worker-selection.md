# Intelligent Worker Selection Protocol

## Purpose
This protocol defines the enhanced decision-making process for Queen orchestrator to autonomously select optimal worker teams based on task requirements, complexity, and scope.

## Worker Selection Matrix

### Domain-to-Worker Mapping

**Template Location**: `.claude/protocols/templates/worker-selection-matrix.yaml`

This matrix defines which workers are required and recommended for different task domains:
- **Required Workers**: Must be spawned for the domain
- **Recommended Workers**: Should be considered based on complexity
- **Domain Categories**: Architecture, security, performance, infrastructure, etc.

## Complexity-Based Worker Augmentation

### Level 1 (Simple Tasks)
- **Worker Count**: 1-2
- **Selection**: Single domain specialist
- **Coordination**: Sequential
- **Example**: "Fix a typo in documentation"

### Level 2 (Moderate Tasks)
- **Worker Count**: 2-3
- **Selection**: Primary + supporting specialists
- **Coordination**: Parallel where possible
- **Example**: "Add a new API endpoint"

### Level 3 (Complex Tasks)
- **Worker Count**: 3-5
- **Selection**: Multi-domain team
- **Always Include**: researcher-worker for complex tasks
- **Coordination**: Phased execution
- **Example**: "Analyze service architecture"

### Level 4 (Critical Tasks)
- **Worker Count**: 5-8
- **Selection**: Full specialist team
- **Always Include**: researcher-worker, architect-worker
- **Coordination**: Research-first, phased execution
- **Example**: "Redesign system architecture"

## Task Analysis Keywords

### Security-Related
- Keywords: security, vulnerability, audit, penetration, encryption, authentication, authorization
- Workers: analyzer-worker, test-worker, backend-worker

### Performance-Related
- Keywords: performance, optimization, speed, latency, throughput, bottleneck
- Workers: analyzer-worker, backend-worker, devops-worker

### Architecture-Related
- Keywords: architecture, design, pattern, structure, scalability, microservice
- Workers: architect-worker, analyzer-worker, devops-worker

### Testing-Related
- Keywords: test, coverage, quality, validation, verification, QA
- Workers: test-worker, analyzer-worker

### Infrastructure-Related
- Keywords: deployment, infrastructure, DevOps, CI/CD, monitoring, scaling
- Workers: devops-worker, backend-worker

### Data-Related
- Keywords: database, data, migration, schema, query, optimization
- Workers: backend-worker, architect-worker

## Queen Decision Algorithm

```python
def select_workers(task_description, complexity_level):
    """
    Enhanced worker selection with intelligent decision-making
    """
    workers = set()
    
    # Step 1: Keyword-based initial selection
    keywords = extract_keywords(task_description.lower())
    for keyword, worker_list in keyword_worker_map.items():
        if keyword in keywords:
            workers.update(worker_list)
    
    # Step 2: Task type detection
    task_type = detect_task_type(task_description)
    if task_type in domain_worker_map:
        workers.update(domain_worker_map[task_type]["required"])
        if complexity_level >= 3:
            workers.update(domain_worker_map[task_type]["recommended"])
    
    # Step 3: Complexity augmentation
    if complexity_level >= 3:
        workers.add("researcher-worker")  # Always for complex tasks
        
    if complexity_level == 4:
        workers.add("architect-worker")  # Always for critical tasks
        
    # Step 4: Comprehensive analysis detection
    if any(word in task_description.lower() for word in 
           ["comprehensive", "analyze", "review", "audit", "assess"]):
        workers.update(["researcher-worker", "architect-worker", "analyzer-worker"])
        if complexity_level >= 3:
            # Add all specialists for comprehensive complex analysis
            workers.update(["backend-worker", "test-worker", "devops-worker"])
    
    # Step 5: Service-specific detection
    if "service" in task_description.lower() or any(
        service in task_description.lower() 
        for service in ["api", "crypto-data", "sara", "frontend", "archon"]):
        workers.update(["backend-worker", "devops-worker"])
        
    # Step 6: Minimum worker enforcement
    min_workers = {
        1: 1,
        2: 2,
        3: 3,
        4: 5
    }
    
    if len(workers) < min_workers.get(complexity_level, 1):
        # Add most versatile workers to meet minimum
        versatile_workers = ["analyzer-worker", "architect-worker", "researcher-worker"]
        for worker in versatile_workers:
            if len(workers) >= min_workers[complexity_level]:
                break
            workers.add(worker)
    
    return list(workers)
```

## Coordination Strategy Selection

### Parallel Execution
- When: Independent analysis domains
- Workers: No inter-dependencies
- Example: analyzer-worker and test-worker analyzing different aspects

### Sequential Execution
- When: Dependent tasks
- Workers: Output of one feeds another
- Example: researcher-worker → implementation workers

### Phased Execution (Recommended for Complex Tasks)
```yaml
Phase 1 - Research:
  workers: [researcher-worker]
  duration: 5-10 minutes
  
Phase 2 - Analysis:
  workers: [analyzer-worker, architect-worker, test-worker]
  duration: 10-15 minutes
  mode: parallel
  
Phase 3 - Deep Dive:
  workers: [backend-worker, devops-worker, frontend-worker]
  duration: 10-15 minutes
  mode: parallel
  
Phase 4 - Synthesis:
  workers: [queen-orchestrator]
  duration: 5-10 minutes
```

## Worker Spawn Verification

### Required Checks
1. Worker prompt file created
2. Worker spawn instruction generated
3. Worker startup event logged within 60 seconds
4. Worker configuration event logged within 90 seconds

### Failure Handling
- If worker doesn't spawn within 2 minutes: Log failure event
- If critical worker fails: Attempt respawn once
- If optional worker fails: Continue without, note in synthesis
- If >50% workers fail: Escalate to user

## Quality Gates

### Worker Selection Quality
- Minimum workers selected for complexity level
- All required domains covered
- Coordination strategy defined
- Spawn verification plan in place

### Team Composition Validation
```python
def validate_team_composition(workers, task_analysis):
    """Ensure selected team can handle task"""
    
    validations = {
        "domain_coverage": check_domain_coverage(workers, task_analysis),
        "complexity_appropriate": len(workers) >= min_workers[complexity],
        "coordination_feasible": check_coordination_feasible(workers),
        "resource_efficient": len(workers) <= max_workers[complexity]
    }
    
    return all(validations.values()), validations
```

## Implementation Notes

1. **Queen Autonomy**: Queen should use this protocol to make intelligent decisions, not just keyword matching
2. **Adaptive Selection**: Adjust worker selection based on task understanding, not rigid rules
3. **Verification Loop**: Always verify workers actually spawned before proceeding
4. **Graceful Degradation**: Continue with available workers if some fail to spawn
5. **Learning Integration**: Track successful team compositions for future reference