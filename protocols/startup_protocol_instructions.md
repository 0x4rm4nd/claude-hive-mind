# Startup Protocol Instructions

## Purpose
The Startup Protocol ensures proper initialization of workers and the Queen orchestrator, including session validation, context loading, and protocol configuration.

## When to Use
- **Always First**: Every worker and Queen MUST run this protocol before any other operations
- **Session Resumption**: When resuming an interrupted session
- **Worker Spawn**: When a new worker is added mid-session
- **Context Refresh**: When reloading context after significant changes

## How to Execute

### Step 1: Import and Initialize
```python
from startup_protocol import StartupProtocol

# Initialize with session info
startup = StartupProtocol(
    session_id="2024-03-15-14-30-auth-implementation",
    worker_type="backend-worker"
)
```

### Step 2: Run Initialization Sequence
```python
# Complete initialization returns configuration
config = startup.initialize()

# Config contains:
# - session_path: Path to session directory
# - context: Loaded context relevant to worker
# - protocols: Available protocol instances
# - state: Current session state
```

### Step 3: Validate and Proceed
```python
if config["validation"]["passed"]:
    # Worker can proceed with tasks
    start_work(config)
else:
    # Handle validation failures
    handle_startup_failure(config["validation"]["errors"])
```

## Parameters

### Required Inputs
- **session_id**: Active session identifier
- **worker_type**: Worker name (queen-orchestrator, backend-worker, etc.)

### Optional Configuration
- **context_tags**: Specific context tags to load
- **protocol_subset**: Load only specific protocols
- **skip_validation**: Bypass validation checks (not recommended)

## Output

### Initialization Configuration
```python
{
    "session_id": "2024-03-15-14-30-auth-implementation",
    "worker_type": "backend-worker",
    "session_path": "Docs/hive-mind/sessions/2024-03-15-14-30-auth-implementation",
    "validation": {
        "passed": True,
        "session_exists": True,
        "worker_authorized": True,
        "protocols_loaded": True
    },
    "context": {
        "loaded_files": ["activeContext.md", "techContext.md"],
        "tags": ["backend", "api", "authentication"],
        "memory_bank_entries": 5
    },
    "protocols": {
        "logging": LoggingProtocol(),
        "monitoring": MonitoringProtocol(),
        "completion": CompletionProtocol(),
        "coordination": CoordinationProtocol()
    },
    "state": {
        "phase": "implementation",
        "workers_active": 3,
        "completion_percentage": 45
    }
}
```

## Integration

### Initialization Sequence
1. **Session Validation**: Verify session exists and is active
2. **Worker Authorization**: Confirm worker is assigned to session
3. **Context Loading**: Load relevant context based on worker tags
4. **Protocol Configuration**: Initialize required protocols
5. **State Synchronization**: Load current session state
6. **Event Registration**: Register worker in EVENTS.jsonl
7. **Health Check**: Verify all systems operational

### Context Loading Strategy
```python
# Context loaded based on worker type:
context_mapping = {
    "backend-worker": ["backend", "api", "database", "security"],
    "frontend-worker": ["frontend", "ui", "react", "ux"],
    "test-worker": ["testing", "quality", "automation"],
    "researcher-worker": ["all"],  # Researchers get full context
    "queen-orchestrator": ["all"]  # Queen gets everything
}
```

## Best Practices

1. **Never Skip Startup**: Always run startup protocol first
2. **Handle Failures Gracefully**: Check validation before proceeding
3. **Log Startup Metrics**: Track initialization time and issues
4. **Cache Context**: Reuse loaded context when appropriate
5. **Verify Protocol Versions**: Ensure protocol compatibility

## Error Handling

### Common Startup Failures
```python
# Session not found
if not config["validation"]["session_exists"]:
    print(f"Session {session_id} not found. Check session ID.")
    
# Worker not authorized
if not config["validation"]["worker_authorized"]:
    print(f"Worker {worker_type} not assigned to this session.")
    
# Protocol loading failed
if not config["validation"]["protocols_loaded"]:
    print("Failed to load required protocols. Check installation.")
```

### Recovery Strategies
- **Missing Session**: Create new session or request correct ID
- **Unauthorized Worker**: Request assignment from Queen
- **Protocol Failures**: Fallback to basic functionality
- **Context Loading Issues**: Proceed with minimal context

## Worker-Specific Initialization

### Backend Worker
```python
startup = StartupProtocol(session_id, "backend-worker")
config = startup.initialize()

# Additional backend-specific setup
db_connection = setup_database(config["context"]["db_config"])
api_routes = load_api_routes(config["context"]["endpoints"])
```

### Frontend Worker
```python
startup = StartupProtocol(session_id, "frontend-worker")
config = startup.initialize()

# Wait for backend if needed
if not config["state"]["backend_ready"]:
    wait_for_backend_ready(config["session_id"])
```

### Queen Orchestrator
```python
startup = StartupProtocol(session_id, "queen-orchestrator")
config = startup.initialize()

# Queen-specific initialization
worker_pool = setup_worker_pool(config["state"]["assigned_workers"])
escalation_chains = configure_escalation(config["context"]["complexity_level"])
```

## Performance Metrics

The protocol tracks:
- **Initialization Time**: Total startup duration
- **Context Load Time**: Time to load context files
- **Protocol Setup Time**: Time to initialize protocols
- **Validation Time**: Time for all validation checks

## Session State Validation

```python
# State validation checks
required_files = ["SESSION.md", "STATE.json", "EVENTS.jsonl"]
required_dirs = ["workers", "research", "context"]

# Automatic repair if files missing
if missing_files:
    startup.repair_session_structure()
```

## Debug Mode

```python
# Enable detailed startup logging
startup = StartupProtocol(session_id, worker_type)
startup.debug = True  # Verbose logging to DEBUG.jsonl
config = startup.initialize()
```

## Example: Complete Worker Startup

```python
from startup_protocol import StartupProtocol
from logging_protocol import LoggingProtocol

# Initialize startup
startup = StartupProtocol(
    session_id="2024-03-15-14-30-payment-api",
    worker_type="backend-worker"
)

# Run initialization
config = startup.initialize()

# Validate startup
if not config["validation"]["passed"]:
    print(f"Startup failed: {config['validation']['errors']}")
    exit(1)

# Setup logging
logger = config["protocols"]["logging"]
logger.log_info("Backend worker initialized successfully")

# Load worker-specific context
api_spec = config["context"].get("api_specification")
db_schema = config["context"].get("database_schema")

# Register with coordination
coord = config["protocols"]["coordination"]
coord.update_worker_status(config["session_id"], "backend-worker", "ready")

# Begin work
print(f"Backend worker ready in session {config['session_id']}")
```

## Notes

- Startup is idempotent - safe to run multiple times
- Context is cached after first load for performance
- Protocol instances are shared across the session
- All paths are automatically resolved relative to project root
- The protocol handles both new and resumed sessions