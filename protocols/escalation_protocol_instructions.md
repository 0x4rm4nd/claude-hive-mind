# Escalation Protocol Instructions

## Purpose
The Escalation Protocol manages the systematic escalation of blocked tasks, unresolved issues, and critical decisions from workers to specialized workers or the Queen orchestrator.

## When to Use
- **Worker Blocked**: When a worker cannot proceed with their task
- **Timeout Exceeded**: When operations exceed complexity-based timeouts
- **Critical Decisions**: When architectural or security decisions are needed
- **Resource Constraints**: When system resources are insufficient
- **Expertise Required**: When specialized knowledge is needed

## How to Execute

### Step 1: Import and Initialize
```python
from escalation_protocol import EscalationProtocol

# Initialize with context
escalation = EscalationProtocol(
    session_id="2024-03-15-14-30-payment-api",
    worker_name="backend-worker",
    complexity_level=3
)
```

### Step 2: Trigger Escalation
```python
# Escalate a blocker
escalation.escalate(
    issue_type="technical_blocker",
    severity="high",
    description="Cannot connect to payment gateway API",
    context={
        "error": "Connection timeout after 3 retries",
        "endpoint": "https://api.payment.com/v2",
        "attempted_solutions": ["retry", "alternate_endpoint", "proxy"]
    },
    suggested_recipient="devops-worker"  # Optional
)
```

### Step 3: Handle Escalation Response
```python
# Check for escalation response
response = escalation.check_response()

if response:
    if response["status"] == "resolved":
        # Apply solution and continue
        apply_solution(response["solution"])
    elif response["status"] == "reassigned":
        # Hand off to designated worker
        handoff_to_worker(response["assigned_to"])
```

## Parameters

### Escalation Types
- **technical_blocker**: Code or system issues
- **dependency_missing**: Required resources unavailable
- **decision_required**: Architectural or business decision needed
- **security_concern**: Security issues requiring review
- **performance_issue**: Performance degradation or limits
- **integration_failure**: External system integration problems

### Severity Levels
- **low**: Can wait, workaround available
- **medium**: Blocking progress, needs attention soon
- **high**: Critical blocker, needs immediate attention
- **critical**: System failure, requires emergency response

### Timeout Configuration (by Complexity)
```python
timeout_config = {
    1: 900,   # 15 minutes for simple tasks
    2: 600,   # 10 minutes for moderate tasks
    3: 300,   # 5 minutes for complex tasks
    4: 120    # 2 minutes for critical tasks
}
```

## Output

### Escalation Record
```json
{
  "id": "esc_001",
  "timestamp": "2024-03-15T14:45:00Z",
  "session_id": "2024-03-15-14-30-payment-api",
  "worker": "backend-worker",
  "issue_type": "technical_blocker",
  "severity": "high",
  "description": "Payment gateway connection failure",
  "context": {
    "error": "Connection timeout",
    "attempts": 3,
    "duration_before_escalation": 180
  },
  "escalation_chain": ["devops-worker", "architect-worker", "queen"],
  "status": "pending",
  "assigned_to": "devops-worker",
  "resolution": null
}
```

## Integration

### Escalation Chains
Default escalation chains by worker type:
```python
escalation_chains = {
    "backend-worker": ["architect-worker", "queen-orchestrator"],
    "frontend-worker": ["designer-worker", "architect-worker", "queen"],
    "test-worker": ["analyzer-worker", "queen-orchestrator"],
    "researcher-worker": ["queen-orchestrator"],
    "devops-worker": ["architect-worker", "queen-orchestrator"]
}
```

### Automatic Escalation Triggers
```python
# Configure automatic escalation
escalation.configure_auto_escalation(
    timeout_threshold=300,  # 5 minutes
    error_threshold=3,      # 3 consecutive errors
    resource_threshold={
        "memory_percent": 90,
        "cpu_percent": 85
    }
)

# Monitor for auto-escalation
escalation.monitor_triggers()
```

## Best Practices

1. **Escalate Early**: Don't waste time on blockers beyond expertise
2. **Provide Context**: Include all relevant information
3. **Suggest Solutions**: Document what you've already tried
4. **Set Expectations**: Indicate urgency and impact
5. **Follow Up**: Check for responses regularly
6. **Document Resolution**: Record how issues were resolved

## Escalation Workflows

### Technical Blocker Escalation
```python
# Worker encounters technical issue
try:
    complex_operation()
except TechnicalError as e:
    # Attempt self-resolution
    if not can_self_resolve(e):
        escalation.escalate(
            issue_type="technical_blocker",
            severity="high",
            description=f"Failed operation: {e}",
            context={
                "stack_trace": traceback.format_exc(),
                "environment": get_environment_info(),
                "attempted_fixes": attempted_solutions
            }
        )
```

### Decision Required Escalation
```python
# Architectural decision needed
if requires_architectural_decision():
    escalation.escalate(
        issue_type="decision_required",
        severity="medium",
        description="Need decision on database schema approach",
        context={
            "options": [
                {"approach": "normalized", "pros": [...], "cons": [...]},
                {"approach": "denormalized", "pros": [...], "cons": [...]}
            ],
            "recommendation": "normalized",
            "impact": "Affects all future queries"
        },
        suggested_recipient="architect-worker"
    )
```

### Security Concern Escalation
```python
# Security issue detected
if security_vulnerability_found():
    escalation.escalate(
        issue_type="security_concern",
        severity="critical",
        description="SQL injection vulnerability detected",
        context={
            "location": "user_service.py:142",
            "vulnerability_type": "SQL Injection",
            "cvss_score": 8.5,
            "affected_endpoints": ["/api/users", "/api/admin"]
        },
        immediate=True  # Bypass normal chain, go straight to top
    )
```

## Response Handling

### Response Types
```python
# Check and handle responses
response = escalation.check_response()

if response:
    match response["type"]:
        case "solution_provided":
            # Implement provided solution
            apply_solution(response["solution"])
            
        case "reassignment":
            # Transfer to another worker
            transfer_context(response["new_worker"])
            
        case "approval_granted":
            # Proceed with proposed approach
            proceed_with_approach()
            
        case "requires_meeting":
            # Schedule synchronous discussion
            log_meeting_requirement(response["participants"])
```

### Resolution Tracking
```python
# Mark escalation as resolved
escalation.mark_resolved(
    escalation_id="esc_001",
    resolution="Applied configuration change to payment gateway",
    implemented_by="devops-worker",
    time_to_resolution_minutes=15
)
```

## Emergency Escalation

### Critical System Failures
```python
# Emergency escalation bypasses normal chains
escalation.emergency_escalate(
    description="Production database down",
    impact="All services affected",
    immediate_action_required="Restore service",
    notify_all=True  # Alerts all available workers
)
```

## Escalation Metrics

### Track Escalation Patterns
```python
# Analyze escalation trends
metrics = escalation.get_metrics()

print(f"Total escalations: {metrics['total']}")
print(f"Average resolution time: {metrics['avg_resolution_minutes']} min")
print(f"Most common issue: {metrics['top_issue_type']}")
print(f"Resolution rate: {metrics['resolution_rate']}%")
```

## Example: Complete Escalation Flow

```python
from escalation_protocol import EscalationProtocol
import time

# Initialize escalation
escalation = EscalationProtocol(
    session_id="2024-03-15-14-30-payment",
    worker_name="backend-worker",
    complexity_level=3
)

# Configure auto-escalation
escalation.configure_auto_escalation(
    timeout_threshold=300,
    error_threshold=3
)

# Main work with escalation handling
max_retries = 3
retry_count = 0

while retry_count < max_retries:
    try:
        # Attempt work
        result = perform_payment_integration()
        break  # Success
        
    except IntegrationError as e:
        retry_count += 1
        
        if retry_count >= max_retries:
            # Escalate after max retries
            esc_id = escalation.escalate(
                issue_type="integration_failure",
                severity="high",
                description="Payment gateway integration failing",
                context={
                    "error": str(e),
                    "retries": retry_count,
                    "gateway": "PaymentProvider API v2",
                    "error_code": e.code
                }
            )
            
            # Wait for response
            timeout = 300  # 5 minutes
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                response = escalation.check_response(esc_id)
                
                if response:
                    if response["status"] == "resolved":
                        # Apply solution
                        print(f"Solution received: {response['solution']}")
                        apply_configuration(response["solution"])
                        break
                    elif response["status"] == "reassigned":
                        # Hand off to specialist
                        print(f"Reassigned to: {response['assigned_to']}")
                        handoff_context(response["assigned_to"])
                        break
                
                time.sleep(30)  # Check every 30 seconds
            else:
                # Timeout - escalate to next level
                escalation.escalate_to_next_level(esc_id)
```

## Troubleshooting

### Common Issues
- **No Response**: Check escalation chain configuration
- **Wrong Recipient**: Verify worker availability and expertise
- **Delayed Response**: Adjust timeout based on complexity
- **Loop Detection**: Prevent circular escalations

### Debug Mode
```python
# Enable escalation debugging
escalation.debug = True  # Verbose logging
escalation.trace_chain = True  # Log full escalation path
```

## Notes

- Escalations are logged in EVENTS.jsonl for audit trail
- Emergency escalations bypass normal chains
- Supports both synchronous and asynchronous resolution
- Automatic timeout-based escalation to next level
- Prevents escalation loops with cycle detection
- Metrics tracked for continuous improvement