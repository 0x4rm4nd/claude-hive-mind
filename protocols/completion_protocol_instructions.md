# Completion Protocol Instructions

## Purpose
The Completion Protocol manages the proper finalization of worker tasks and session completion, ensuring all outputs are captured, formatted, and saved according to SmartWalletFX standards.

## When to Use
- **Workers**: Use when completing any assigned task to properly format and save results
- **Queen**: Use when finalizing a session and aggregating worker outputs
- **Always Required**: Every worker MUST use this protocol before marking their task as complete

## How to Execute

### Step 1: Import and Initialize
```python
from completion_protocol import CompletionProtocol

# Initialize with worker context
completion = CompletionProtocol(config)
```

### Step 2: Prepare Results
Structure your worker's results in the expected format:
```python
results = {
    "findings": [...],           # List of discovered items/issues
    "recommendations": [...],     # Actionable recommendations
    "evidence": [...],           # Supporting evidence/data
    "metrics": {...},            # Performance/quality metrics
    "custom_data": {...}         # Worker-specific data
}
```

### Step 3: Finalize Output
```python
# Finalize and save results
finalized = completion.finalize(results)

# Archive if needed (Level 3+ tasks)
if task_complexity >= 3:
    completion.archive_session()
```

## Parameters

### Required Inputs
- **results**: Dictionary containing worker findings, recommendations, and evidence
- **config**: Worker configuration with session_id and worker_type

### Configuration Options
- **archive_level**: Determines what gets archived (1=minimal, 2=standard, 3=comprehensive)
- **summary_format**: Executive summary style (brief/detailed/technical)
- **metrics_enabled**: Whether to calculate and include performance metrics

## Output

### File Locations
- **Worker Output**: `Docs/hive-mind/sessions/{session_id}/workers/{worker_name}/FINAL_REPORT.json`
- **Session Summary**: `Docs/hive-mind/sessions/{session_id}/COMPLETION_SUMMARY.md`
- **Archive**: `Docs/hive-mind/sessions/{session_id}/archive/`

### Output Format
```json
{
  "worker": "backend-worker",
  "session_id": "2024-03-15-14-30-api-refactor",
  "timestamp": "2024-03-15T16:45:00",
  "status": "completed",
  "summary": {
    "total_changes": 15,
    "files_modified": 8,
    "tests_passed": 42,
    "completion_percentage": 100
  },
  "findings": [...],
  "recommendations": [...],
  "evidence": [...],
  "metrics": {...}
}
```

## Integration

### Works With
- **Logging Protocol**: Automatically logs completion events
- **Monitoring Protocol**: Updates session metrics
- **Synthesis Protocol**: Provides input for cross-worker synthesis
- **Session Management**: Updates STATE.json with completion status

### Event Generation
The protocol automatically generates these events:
- `worker_completed`: When individual worker finishes
- `session_completed`: When all workers finish
- `archive_created`: When session is archived

## Best Practices

1. **Always Include Evidence**: Support findings with concrete file references or data
2. **Be Specific in Recommendations**: Include exact file paths and code snippets
3. **Calculate Meaningful Metrics**: Track metrics relevant to your worker's domain
4. **Test Before Finalizing**: Ensure all tests pass before calling finalize()
5. **Document Blockers**: If incomplete, clearly document what prevented completion

## Error Handling

The protocol handles these scenarios:
- Missing required fields in results
- Invalid session configurations
- File system write failures
- Concurrent worker completions

## Example Usage

### Backend Worker Completion
```python
from completion_protocol import CompletionProtocol

# After implementing changes
results = {
    "findings": [
        {"type": "api_endpoint", "path": "/api/v2/users", "status": "created"},
        {"type": "database_migration", "file": "migrations/001_users.sql", "status": "applied"}
    ],
    "recommendations": [
        {"action": "add_rate_limiting", "endpoint": "/api/v2/users", "priority": "high"},
        {"action": "implement_caching", "component": "user_service", "priority": "medium"}
    ],
    "evidence": [
        {"test_results": "all_passing", "coverage": "85%"},
        {"performance": "response_time_improved_by_30%"}
    ],
    "metrics": {
        "lines_added": 450,
        "lines_removed": 120,
        "test_coverage": 85,
        "api_endpoints_created": 3
    }
}

completion = CompletionProtocol(worker_config)
final_output = completion.finalize(results)
print(f"Completion saved to: {final_output['output_path']}")
```

## Quality Gates

Before calling finalize(), ensure:
- [ ] All assigned tasks are complete or explicitly marked as blocked
- [ ] Tests are passing
- [ ] Documentation is updated
- [ ] Code follows project standards
- [ ] Security considerations addressed
- [ ] Performance requirements met

## Notes

- The protocol is idempotent - calling finalize() multiple times is safe
- Incomplete tasks should still call finalize() with partial results and blockers documented
- Archive level is determined by task complexity, not manually set
- The protocol preserves all intermediate work in the session directory