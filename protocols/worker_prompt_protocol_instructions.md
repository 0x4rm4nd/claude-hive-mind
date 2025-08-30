# Worker Prompt Protocol Instructions

## Purpose
The Worker Prompt Protocol manages dynamic prompt generation and context injection for workers, ensuring each worker receives appropriate context, instructions, and constraints based on their role and the current task.

## When to Use
- **Worker Initialization**: When spawning new workers with task-specific prompts
- **Context Updates**: When worker context needs to be refreshed
- **Role Switching**: When a worker's responsibilities change mid-session
- **Prompt Enhancement**: When adding specific instructions or constraints

## How to Execute

### Step 1: Import and Initialize
```python
from worker_prompt_protocol import WorkerPromptProtocol

# Initialize with worker context
prompt_protocol = WorkerPromptProtocol(
    session_id="2024-03-15-14-30-auth-api",
    worker_type="backend-worker",
    complexity_level=3
)
```

### Step 2: Generate Worker Prompt
```python
# Generate complete prompt for worker
prompt = prompt_protocol.generate_prompt(
    task_description="Implement OAuth2 authentication",
    context_tags=["authentication", "security", "api"],
    additional_instructions=[
        "Follow OWASP security guidelines",
        "Implement rate limiting",
        "Add comprehensive logging"
    ]
)
```

### Step 3: Apply Dynamic Context
```python
# Update prompt with runtime context
enhanced_prompt = prompt_protocol.enhance_with_context(
    base_prompt=prompt,
    runtime_context={
        "api_version": "v2",
        "database": "PostgreSQL",
        "existing_endpoints": ["/api/v2/users", "/api/v2/roles"]
    }
)
```

## Parameters

### Worker Types and Default Prompts
```python
worker_prompts = {
    "backend-worker": {
        "focus": ["API development", "database operations", "business logic"],
        "tools": ["Read", "Edit", "MultiEdit", "Bash"],
        "constraints": ["SOLID principles", "RESTful design", "Security-first"]
    },
    "frontend-worker": {
        "focus": ["UI components", "state management", "user experience"],
        "tools": ["Read", "Edit", "MultiEdit", "Bash"],
        "constraints": ["Responsive design", "Accessibility", "Performance"]
    },
    "test-worker": {
        "focus": ["Unit testing", "integration testing", "test coverage"],
        "tools": ["Read", "Edit", "Bash", "pytest"],
        "constraints": ["80% coverage minimum", "Test isolation", "CI/CD ready"]
    }
}
```

### Context Injection Levels
- **minimal**: Basic task description only
- **standard**: Task + relevant context files
- **comprehensive**: Full context including history and patterns
- **specialized**: Custom context for specific domains

## Output

### Generated Prompt Structure
```markdown
# Worker: {worker_type}
## Session: {session_id}

### Your Role
You are the {worker_type} for this session. Your primary responsibilities include:
- {responsibility_1}
- {responsibility_2}
- {responsibility_3}

### Current Task
**Description**: {task_description}
**Complexity**: Level {complexity_level}
**Priority**: {priority}

### Context
{injected_context}

### Technical Requirements
- {requirement_1}
- {requirement_2}

### Constraints and Guidelines
- {constraint_1}
- {constraint_2}

### Available Tools
You have access to the following tools:
- {tool_1}: {tool_description}
- {tool_2}: {tool_description}

### Success Criteria
- [ ] {criterion_1}
- [ ] {criterion_2}

### Communication Protocol
- Check EVENTS.jsonl every {interval} seconds
- Update status via coordination protocol
- Escalate blockers within {timeout} minutes
```

## Integration

### Dynamic Context Loading
```python
# Load context based on worker needs
context = prompt_protocol.load_relevant_context(
    worker_type="backend-worker",
    tags=["api", "authentication"],
    include_history=True,
    max_context_size=5000  # tokens
)
```

### Prompt Templates
```python
# Use predefined templates
template = prompt_protocol.get_template("feature_development")

# Customize template
customized = prompt_protocol.customize_template(
    template=template,
    customizations={
        "technology_stack": ["Python", "FastAPI", "PostgreSQL"],
        "coding_standards": "PEP 8",
        "testing_framework": "pytest"
    }
)
```

## Best Practices

1. **Context Relevance**: Only include context relevant to the task
2. **Clear Instructions**: Be specific about expectations
3. **Tool Awareness**: Ensure worker knows available tools
4. **Success Metrics**: Define measurable success criteria
5. **Escalation Paths**: Include clear escalation instructions

## Advanced Features

### Adaptive Prompting
```python
# Adjust prompt based on worker performance
if worker_struggling:
    enhanced_prompt = prompt_protocol.add_guidance(
        prompt=current_prompt,
        guidance_type="step_by_step",
        examples=relevant_examples
    )
```

### Multi-Stage Prompting
```python
# Generate phase-specific prompts
phases = ["research", "implementation", "testing", "documentation"]

for phase in phases:
    phase_prompt = prompt_protocol.generate_phase_prompt(
        worker_type="backend-worker",
        phase=phase,
        previous_phase_output=last_output
    )
```

### Collaborative Prompting
```python
# Generate prompts for worker collaboration
collab_prompt = prompt_protocol.generate_collaboration_prompt(
    primary_worker="backend-worker",
    supporting_worker="frontend-worker",
    handoff_point="API endpoints ready",
    shared_context=api_specification
)
```

## Prompt Optimization

### Token Efficiency
```python
# Optimize prompt for token usage
optimized = prompt_protocol.optimize_prompt(
    prompt=original_prompt,
    max_tokens=2000,
    preserve_critical=True
)
```

### Context Pruning
```python
# Remove redundant context
pruned = prompt_protocol.prune_context(
    context=full_context,
    relevance_threshold=0.7,
    keep_recent=True
)
```

## Example: Complete Prompt Generation

```python
from worker_prompt_protocol import WorkerPromptProtocol

# Initialize protocol
prompt_proto = WorkerPromptProtocol(
    session_id="2024-03-15-14-30-payment",
    worker_type="backend-worker",
    complexity_level=3
)

# Load base template
template = prompt_proto.get_template("api_development")

# Load relevant context
context = prompt_proto.load_relevant_context(
    tags=["payment", "stripe", "api"],
    include_patterns=True,
    include_memory_bank=True
)

# Generate base prompt
base_prompt = prompt_proto.generate_prompt(
    task_description="Integrate Stripe payment processing",
    template=template,
    context=context
)

# Add specific requirements
enhanced_prompt = prompt_proto.add_requirements(
    prompt=base_prompt,
    requirements=[
        "PCI compliance required",
        "Implement webhook handling",
        "Add idempotency keys",
        "Include comprehensive error handling"
    ]
)

# Add success criteria
final_prompt = prompt_proto.add_success_criteria(
    prompt=enhanced_prompt,
    criteria=[
        "All payment flows tested",
        "Webhook signature verification implemented",
        "Error recovery mechanisms in place",
        "Documentation complete"
    ]
)

# Optimize for token efficiency
optimized_prompt = prompt_proto.optimize_prompt(
    prompt=final_prompt,
    max_tokens=3000
)

# Validate prompt completeness
validation = prompt_proto.validate_prompt(optimized_prompt)
if validation["is_complete"]:
    print("Prompt ready for worker")
else:
    print(f"Missing: {validation['missing_elements']}")

# Save prompt for audit
prompt_proto.save_prompt(
    prompt=optimized_prompt,
    worker="backend-worker",
    timestamp=datetime.now()
)
```

## Prompt Validation

### Completeness Checks
```python
# Ensure prompt has all required elements
required_elements = [
    "task_description",
    "success_criteria",
    "available_tools",
    "escalation_path",
    "communication_protocol"
]

validation = prompt_protocol.validate_completeness(
    prompt=generated_prompt,
    required=required_elements
)
```

### Clarity Assessment
```python
# Check prompt clarity
clarity = prompt_protocol.assess_clarity(prompt)

if clarity["score"] < 0.8:
    # Enhance clarity
    clearer_prompt = prompt_protocol.enhance_clarity(prompt)
```

## Troubleshooting

### Common Issues
- **Context Overflow**: Reduce context size or prioritize relevant items
- **Ambiguous Instructions**: Use specific, measurable criteria
- **Missing Tools**: Ensure all required tools are listed
- **Unclear Escalation**: Define explicit escalation triggers

### Debug Mode
```python
# Enable prompt debugging
prompt_protocol.debug = True  # Shows prompt construction steps
prompt_protocol.show_token_count = True  # Display token usage
```

## Notes

- Prompts are versioned for traceability
- Supports both static and dynamic prompt generation
- Integrates with memory bank for historical context
- Automatic prompt optimization for token efficiency
- Thread-safe for concurrent prompt generation
- All prompts logged for audit and improvement