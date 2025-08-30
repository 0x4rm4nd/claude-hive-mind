# Logging Protocol Instructions

## Purpose
The Logging Protocol provides structured, consistent logging across all workers and the Queen orchestrator, ensuring comprehensive audit trails and debugging capabilities.

## When to Use
- **Every Operation**: Log all significant actions and decisions
- **Error Tracking**: Capture all errors with context
- **Performance Monitoring**: Log timing and resource metrics
- **Audit Requirements**: Create immutable audit trail for compliance
- **Debug Sessions**: Enhanced logging for troubleshooting

## How to Execute

### Step 1: Import and Initialize
```python
from logging_protocol import LoggingProtocol

# Initialize with session context
logger = LoggingProtocol(
    session_id="2024-03-15-14-30-auth-api",
    worker_name="backend-worker"
)
```

### Step 2: Log Events at Appropriate Levels
```python
# Informational logging
logger.log_info("Starting API endpoint creation")

# Warning for potential issues
logger.log_warning("Database connection pool near capacity", 
                   {"connections": 95, "max": 100})

# Error logging with context
logger.log_error("Failed to create user", 
                 {"error": str(e), "user_data": user_dict})

# Debug for detailed troubleshooting
logger.log_debug("SQL query executed", 
                 {"query": sql, "duration_ms": 45})

# Critical for system failures
logger.log_critical("Database connection lost", 
                   {"retry_attempts": 3, "next_action": "escalate"})
```

## Parameters

### Log Levels
- **DEBUG**: Detailed debugging information
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for failures
- **CRITICAL**: Critical failures requiring immediate attention

### DEBUG.jsonl Entry Structure
```python
{
    "timestamp": "2025-01-15T10:30:00Z",
    "level": "INFO",
    "agent": "backend-worker",
    "message": "API endpoint created successfully",
    "details": {
        "endpoint": "/api/v2/auth/login",
        "method": "POST",
        "duration_ms": 1250
    },
    "context": {
        "file": "auth_service.py",
        "function": "create_login_endpoint",
        "line": 142
    }
}
```

## Output

### Log File Locations
- **Worker Logs**: `Docs/hive-mind/sessions/{session_id}/workers/{worker_name}/worker.log`
- **Session Log**: `Docs/hive-mind/sessions/{session_id}/SESSION.log`
- **Debug Log**: `Docs/hive-mind/sessions/{session_id}/DEBUG.jsonl`
- **Audit Trail**: `Docs/hive-mind/sessions/{session_id}/AUDIT.jsonl`

### Log Formats
- **.log files**: Human-readable format
- **.jsonl files**: Structured JSON Lines for parsing
- **AUDIT.jsonl**: Immutable, signed entries for compliance

## Integration

### Automatic Integration
The logging protocol automatically integrates with:
- **Coordination Protocol**: Logs all coordination events
- **Monitoring Protocol**: Provides metrics for monitoring
- **Completion Protocol**: Includes logs in final reports
- **Escalation Protocol**: Triggers escalation on critical logs

### Structured Logging Methods

#### Operation Logging
```python
# Log operation start and end
operation_id = logger.start_operation("create_user_service")
# ... perform operation ...
logger.end_operation(operation_id, success=True, 
                    metrics={"users_created": 5})
```

#### Performance Logging
```python
# Log with timing
with logger.timed_operation("database_query"):
    results = db.execute(query)
# Automatically logs duration
```

#### Error Context Logging
```python
try:
    risky_operation()
except Exception as e:
    logger.log_exception("Operation failed", 
                        exception=e,
                        context={"input": data})
```

## Best Practices

1. **Log Early and Often**: Capture state before and after operations
2. **Include Context**: Always provide relevant data with logs
3. **Use Appropriate Levels**: Choose correct severity level
4. **Structured Data**: Use dictionaries for data, not strings
5. **Avoid Sensitive Data**: Never log passwords, tokens, or PII
6. **Batch Related Logs**: Group related operations together

## Advanced Features

### Log Aggregation
```python
# Aggregate logs for summary
summary = logger.aggregate_logs(
    level="ERROR",
    time_range=(start_time, end_time),
    worker="backend-worker"
)
```

### Log Filtering
```python
# Filter logs by criteria
errors = logger.filter_logs(
    level=["ERROR", "CRITICAL"],
    pattern="database",
    last_n_minutes=30
)
```

### Log Rotation
```python
# Automatic rotation when log exceeds size
logger.set_rotation(
    max_size_mb=10,
    max_files=5,
    compress=True
)
```

### Custom Fields
```python
# Add custom fields to all logs
logger.set_context({
    "environment": "production",
    "version": "2.1.0",
    "feature_flag": "new_auth_enabled"
})
```

## Error Handling

### Logging Failures
The protocol handles logging failures gracefully:
```python
# Fallback to stderr if file writing fails
# Buffering for temporary file system issues
# Retry logic for network logging endpoints
```

### Recovery Mechanisms
- **Local Buffer**: Stores logs in memory if file system unavailable
- **Fallback Locations**: Alternative log directories
- **Compression**: Automatic compression of old logs
- **Cleanup**: Removes logs older than retention period

## Performance Monitoring

### Metrics Logged
```python
# Automatic performance metrics
logger.log_metrics({
    "operation": "api_request",
    "duration_ms": 145,
    "memory_mb": 256,
    "cpu_percent": 45,
    "success": True
})
```

### Performance Thresholds
```python
# Alert on performance issues
logger.set_performance_thresholds({
    "api_response_ms": 1000,
    "memory_mb": 512,
    "error_rate_percent": 5
})
```

## Debug Mode

### Enhanced Debugging
```python
# Enable verbose debug logging
logger.set_debug_mode(True)

# Debug mode includes:
# - Stack traces for all errors
# - Input/output for all operations  
# - Timing for every function call
# - Memory snapshots
```

### Debug Helpers
```python
# Log variable state
logger.debug_vars(locals())

# Log object state
logger.debug_object(my_object)

# Log call stack
logger.debug_stack()
```

## Example: Complete Logging Flow

```python
from logging_protocol import LoggingProtocol

# Initialize logger
logger = LoggingProtocol("2024-03-15-14-30-api", "backend-worker")

# Set context for all logs
logger.set_context({"component": "auth_service"})

# Log operation start
logger.log_info("Starting authentication service setup")

try:
    # Timed operation
    with logger.timed_operation("database_setup"):
        setup_database()
    
    # Log successful step
    logger.log_info("Database configured", {"tables_created": 5})
    
    # Create API endpoints
    endpoints = []
    for endpoint in api_spec:
        logger.log_debug(f"Creating endpoint: {endpoint['path']}")
        
        try:
            ep = create_endpoint(endpoint)
            endpoints.append(ep)
            logger.log_info(f"Endpoint created", {"path": ep.path})
            
        except Exception as e:
            logger.log_error(f"Failed to create endpoint", 
                           {"endpoint": endpoint, "error": str(e)})
            raise
    
    # Log completion metrics
    logger.log_metrics({
        "total_endpoints": len(endpoints),
        "setup_duration_ms": 2500,
        "status": "success"
    })
    
except Exception as e:
    # Log critical failure
    logger.log_critical("Authentication service setup failed",
                       {"error": str(e), "stack": traceback.format_exc()})
    
    # Trigger escalation
    logger.escalate("Backend setup failed, need assistance")
    
finally:
    # Always log completion
    logger.log_info("Authentication service setup completed")
    
    # Generate summary
    summary = logger.generate_summary()
    logger.save_summary(summary)
```

## Log Analysis Tools

### Built-in Analysis
```python
# Analyze error patterns
patterns = logger.analyze_errors(
    time_range="last_hour",
    group_by="error_type"
)

# Generate report
report = logger.generate_report(
    include=["errors", "warnings", "metrics"],
    format="markdown"
)
```

## Notes

- All timestamps are UTC in ISO format
- Logs are immutable once written (append-only)
- Automatic cleanup of logs older than 30 days
- Thread-safe for concurrent logging
- Supports both synchronous and asynchronous logging
- Integrates with external logging services if configured
