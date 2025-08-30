# Synthesis Protocol Instructions

## Purpose
The Synthesis Protocol aggregates, analyzes, and synthesizes outputs from multiple workers into cohesive insights, architectural decisions, and actionable recommendations.

## When to Use
- **Multi-Worker Sessions**: When multiple workers contribute to a task
- **Research Consolidation**: Combining findings from research activities
- **Architecture Decisions**: Synthesizing technical options into decisions
- **Knowledge Extraction**: Creating reusable patterns from implementations
- **Session Completion**: Final synthesis of all session outputs

## How to Execute

### Step 1: Import and Initialize
```python
from synthesis_protocol import SynthesisProtocol

# Initialize with session context
synthesis = SynthesisProtocol(
    session_id="2024-03-15-14-30-microservices",
    synthesizer="queen-orchestrator"  # or architect-worker
)
```

### Step 2: Collect Worker Outputs
```python
# Gather outputs from all workers
outputs = synthesis.collect_worker_outputs()

# Or collect specific workers
outputs = synthesis.collect_outputs_from([
    "researcher-worker",
    "backend-worker", 
    "frontend-worker"
])
```

### Step 3: Perform Synthesis
```python
# Synthesize findings
result = synthesis.synthesize(
    outputs=outputs,
    synthesis_type="technical_decision",
    focus_areas=["architecture", "performance", "security"]
)

# Save synthesis
synthesis.save_synthesis(result)
```

## Parameters

### Synthesis Types
- **technical_decision**: Architecture and technology choices
- **research_findings**: Consolidated research insights
- **implementation_patterns**: Reusable code patterns
- **lessons_learned**: Session insights and improvements
- **final_report**: Comprehensive session summary

### Focus Areas
- **architecture**: System design and structure
- **performance**: Speed, efficiency, optimization
- **security**: Vulnerabilities, hardening, compliance
- **user_experience**: UI/UX insights and improvements
- **scalability**: Growth handling and limits
- **maintainability**: Code quality and technical debt

## Output

### Synthesis Document Structure
```markdown
# Synthesis Report: {title}

## Executive Summary
{high-level summary of key findings and decisions}

## Key Findings
1. {Major finding with evidence}
2. {Another finding with impact}
3. {Critical discovery with implications}

## Synthesized Insights
### Architecture Decisions
- **Decision**: {what was decided}
- **Rationale**: {why this approach}
- **Trade-offs**: {pros and cons}
- **Implementation**: {how to proceed}

### Performance Optimizations
- {Optimization with measured impact}

### Security Considerations
- {Security finding with mitigation}

## Recommendations
### Immediate Actions
1. {High priority action}
2. {Another urgent item}

### Future Considerations
- {Long-term improvement}
- {Technical debt item}

## Patterns Extracted
### Pattern: {pattern name}
**Context**: {when to use}
**Solution**: {the pattern}
**Example**: {code or approach}

## Metrics and Evidence
- {Quantitative data supporting findings}
- {Performance measurements}
- {Quality metrics}

## Appendices
### A. Worker Contributions
- {Worker}: {summary of contribution}

### B. Supporting Data
- {Links to detailed evidence}
```

## Integration

### Multi-Source Synthesis
```python
# Combine different types of inputs
synthesis.add_source("research", research_findings)
synthesis.add_source("implementation", code_changes)
synthesis.add_source("testing", test_results)
synthesis.add_source("monitoring", performance_metrics)

# Perform cross-source synthesis
integrated_insights = synthesis.cross_synthesize()
```

### Pattern Extraction
```python
# Extract reusable patterns
patterns = synthesis.extract_patterns(
    from_implementations=["backend-worker", "frontend-worker"],
    pattern_types=["architectural", "coding", "testing"]
)

# Save to pattern library
for pattern in patterns:
    synthesis.save_pattern(pattern)
```

## Best Practices

1. **Wait for Completion**: Ensure all workers finish before synthesis
2. **Validate Inputs**: Check worker outputs for completeness
3. **Cross-Reference**: Verify findings across multiple sources
4. **Quantify Impact**: Include metrics and measurements
5. **Extract Patterns**: Identify reusable solutions
6. **Document Rationale**: Explain why, not just what

## Advanced Features

### Conflict Resolution
```python
# Handle conflicting recommendations
if synthesis.has_conflicts():
    conflicts = synthesis.identify_conflicts()
    
    for conflict in conflicts:
        resolution = synthesis.resolve_conflict(
            conflict,
            strategy="evidence_based",  # or "consensus", "authority"
            arbiter="architect-worker"
        )
        synthesis.document_resolution(resolution)
```

### Quality Assessment
```python
# Assess synthesis quality
quality = synthesis.assess_quality()

quality_metrics = {
    "completeness": 0.95,  # All workers contributed
    "coherence": 0.88,     # Logical consistency
    "evidence": 0.92,      # Well-supported findings
    "actionability": 0.85  # Clear next steps
}

if quality["overall"] < 0.8:
    synthesis.enhance_synthesis()  # Automated improvement
```

### Knowledge Base Integration
```python
# Update knowledge base with synthesis
synthesis.update_knowledge_base(
    entries=[
        {"type": "pattern", "content": architectural_pattern},
        {"type": "decision", "content": tech_decision},
        {"type": "lesson", "content": lesson_learned}
    ],
    tags=["microservices", "authentication", "performance"]
)
```

## Synthesis Strategies

### Bottom-Up Synthesis
```python
# Start from details, build to insights
synthesis.configure(strategy="bottom_up")

# 1. Collect raw data
raw_data = synthesis.collect_raw_outputs()

# 2. Identify patterns
patterns = synthesis.find_patterns(raw_data)

# 3. Abstract insights
insights = synthesis.abstract_insights(patterns)

# 4. Form conclusions
conclusions = synthesis.form_conclusions(insights)
```

### Top-Down Synthesis
```python
# Start from goals, validate with evidence
synthesis.configure(strategy="top_down")

# 1. Define hypotheses
hypotheses = synthesis.define_hypotheses(session_goals)

# 2. Gather evidence
evidence = synthesis.gather_evidence(hypotheses)

# 3. Validate or refute
validated = synthesis.validate_hypotheses(evidence)

# 4. Synthesize findings
findings = synthesis.synthesize_validated(validated)
```

### Iterative Refinement
```python
# Multiple rounds of synthesis
for iteration in range(3):
    # Perform synthesis
    result = synthesis.synthesize(outputs)
    
    # Get feedback
    feedback = synthesis.get_feedback(result)
    
    # Refine based on feedback
    if feedback["needs_refinement"]:
        synthesis.refine(result, feedback)
    else:
        break
```

## Example: Complete Synthesis Flow

```python
from synthesis_protocol import SynthesisProtocol

# Initialize synthesis
synthesis = SynthesisProtocol(
    session_id="2024-03-15-14-30-auth-system",
    synthesizer="architect-worker"
)

# Collect all worker outputs
outputs = synthesis.collect_worker_outputs()

# Validate completeness
if not synthesis.validate_outputs(outputs):
    missing = synthesis.identify_missing_outputs()
    print(f"Warning: Missing outputs from {missing}")

# Configure synthesis parameters
synthesis.configure(
    strategy="bottom_up",
    focus_areas=["security", "performance", "scalability"],
    output_format="technical_report"
)

# Perform multi-stage synthesis
# Stage 1: Individual worker synthesis
worker_summaries = {}
for worker, output in outputs.items():
    summary = synthesis.summarize_worker_output(worker, output)
    worker_summaries[worker] = summary

# Stage 2: Cross-worker pattern identification
patterns = synthesis.identify_cross_worker_patterns(worker_summaries)

# Stage 3: Technical decision synthesis
decisions = synthesis.synthesize_decisions(
    worker_summaries=worker_summaries,
    patterns=patterns,
    constraints=project_constraints
)

# Stage 4: Generate recommendations
recommendations = synthesis.generate_recommendations(
    decisions=decisions,
    priority_matrix=priority_criteria
)

# Stage 5: Create final synthesis
final_synthesis = synthesis.create_final_synthesis(
    summaries=worker_summaries,
    patterns=patterns,
    decisions=decisions,
    recommendations=recommendations
)

# Quality check
quality = synthesis.assess_quality(final_synthesis)
if quality["score"] < 0.8:
    # Enhance synthesis
    final_synthesis = synthesis.enhance_synthesis(final_synthesis)

# Save outputs
synthesis.save_synthesis(final_synthesis)
synthesis.update_memory_bank(final_synthesis)
synthesis.extract_to_pattern_library(patterns)

# Generate visualizations
synthesis.generate_visualization(
    type="decision_tree",
    data=decisions,
    output_path="decisions.svg"
)

# Create executive summary
exec_summary = synthesis.create_executive_summary(final_synthesis)
print(exec_summary)
```

## Visualization and Reporting

### Generate Reports
```python
# Generate different report formats
synthesis.generate_report(
    format="markdown",  # or "html", "pdf", "json"
    include=[
        "executive_summary",
        "key_findings",
        "decisions",
        "recommendations",
        "metrics"
    ],
    audience="technical"  # or "executive", "stakeholder"
)
```

### Create Visualizations
```python
# Generate visual representations
synthesis.create_visualization(
    type="mind_map",     # or "flow_chart", "decision_tree"
    data=synthesis_result,
    style="technical"
)
```

## Quality Assurance

### Synthesis Validation
```python
# Validate synthesis quality
validation = synthesis.validate()

validation_checks = {
    "completeness": "All workers represented",
    "consistency": "No contradictory findings",
    "evidence": "All claims supported",
    "actionability": "Clear next steps provided",
    "clarity": "Well-organized and readable"
}
```

### Peer Review
```python
# Request peer review
review = synthesis.request_review(
    reviewer="architect-worker",
    focus_areas=["technical_accuracy", "completeness"]
)

# Incorporate feedback
if review["changes_requested"]:
    synthesis.incorporate_feedback(review["feedback"])
```

## Notes

- Synthesis is non-destructive - original outputs preserved
- Supports incremental synthesis as workers complete
- Automatic conflict detection and resolution
- Integrates with memory bank for knowledge persistence
- Generates both human-readable and machine-parseable outputs
- Thread-safe for concurrent synthesis operations