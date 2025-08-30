# STATE.json Management Protocol

## Purpose
Defines the structure, update mechanisms, and accuracy requirements for STATE.json to ensure reliable session state tracking and coordination.

## STATE.json Structure v2.0

**Template Location**: `.claude/templates/state-v2-template.json`

The STATE.json structure defines comprehensive session state tracking with the following key sections:
- **Version & Identification**: Protocol version, session ID, and task description
- **Timestamps**: Creation, updates, heartbeats, and phase transitions
- **Coordination Status**: Worker planning, spawning, and execution tracking
- **Worker States**: Individual worker status, metrics, and compliance (see `templates/worker-state-template.json`)
- **Queen Decisions**: Complexity assessment, worker selection rationale, and execution plan
- **Progress Tracking**: Research and implementation progress with quality gates
- **Metrics**: Session-wide performance and efficiency metrics
- **Session Metadata**: Environment configuration and recovery capabilities

## Update Mechanisms

### Atomic Update Function

**Function Template**: `.claude/templates/state-management-functions.py`

#### Function: `update_state(session_id, updates, merge_strategy="deep")`
- **Purpose**: Atomically update STATE.json with conflict resolution
- **Parameters**:
  - `session_id`: Active session identifier
  - `updates`: Dictionary of updates to apply
  - `merge_strategy`: "deep" for nested merge, "shallow" for top-level merge
- **Returns**: Updated state dictionary
- **Implementation**: Uses file locking (fcntl) for atomic operations

### Required Update Points

#### Queen Updates
1. **Session Creation**: Initialize full structure
2. **Worker Planning**: Update `queen_decisions` and `coordination_status.workers_planned`
3. **Worker Spawning**: Update `coordination_status.spawn_attempts`
4. **Phase Transitions**: Update `coordination_status.phase` and timestamps
5. **Synthesis Start/Complete**: Update research_progress and quality_gates

#### Worker Updates
1. **Worker Spawn**: Update `worker_states[worker].status` to "active"
2. **Configuration Complete**: Update protocol_compliance flags
3. **Progress Updates**: Update metrics and last_heartbeat
4. **Task Completion**: Update status, outputs, and metrics
5. **Failure/Timeout**: Update status to "failed" with error details

## Validation Rules

### State Consistency Rules
1. **Worker Count Consistency**: 
   - `len(workers_spawned) <= len(workers_planned)`
   - `workers_active ⊆ workers_spawned`
   - `workers_completed ⊆ workers_spawned`

2. **Phase Progression**:
   - Phases must progress: initializing → planning → spawning → executing → synthesizing → complete
   - Cannot skip phases
   - Can transition to "failed" from any phase

3. **Timestamp Consistency**:
   - `created_at < updated_at`
   - `spawned_at < last_update` for each worker
   - Phase transition times must be sequential

4. **Worker State Validation**:

   **Function Template**: `.claude/templates/state-management-functions.py`
   
   #### Function: `validate_worker_state(worker_state)`
   - Validates required fields presence
   - Checks status validity
   - Ensures metrics consistency
   - Verifies outputs for completed workers
   - Returns tuple: (is_valid, validation_details)

## Recovery Mechanisms

### State Corruption Recovery

**Function Template**: `.claude/templates/state-management-functions.py`

#### Function: `recover_state(session_id)`
- **Purpose**: Recover STATE.json from EVENTS.jsonl if corrupted
- **Parameters**: `session_id` - Session to recover
- **Returns**: Rebuilt state dictionary from event log
- **Usage**: Emergency recovery when STATE.json is corrupted or missing

### Heartbeat Monitoring

**Function Template**: `.claude/templates/state-management-functions.py`

#### Function: `check_worker_health(session_id)`
- **Purpose**: Monitor worker health via heartbeat
- **Parameters**: `session_id` - Session to monitor
- **Returns**: List of unhealthy workers with timeout details
- **Timeout**: 5 minutes without heartbeat marks worker as unhealthy

## Best Practices

1. **Always Use Atomic Updates**: Never read-modify-write without locking
2. **Validate Before Update**: Check state consistency before writing
3. **Log All Updates**: Every state change should have corresponding event
4. **Regular Heartbeats**: Active workers should update heartbeat every 60 seconds
5. **Fail Fast**: Mark workers as failed quickly to enable recovery
6. **Preserve History**: Never delete old state, archive if needed
