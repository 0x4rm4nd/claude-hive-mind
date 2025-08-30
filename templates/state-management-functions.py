"""
State Management Functions Template
Functions for STATE.json atomic updates and recovery.
Reference from state-management-protocol.md
"""

import json
import fcntl
from datetime import datetime

def update_state(session_id, updates, merge_strategy="deep"):
    """
    Atomically update STATE.json with conflict resolution
    """
    state_path = f"Docs/hive-mind/sessions/{session_id}/STATE.json"
    
    # Lock file for atomic update
    with open(state_path, 'r+') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        
        # Read current state
        current_state = json.load(f)
        
        # Apply updates
        if merge_strategy == "deep":
            updated_state = deep_merge(current_state, updates)
        else:
            updated_state = {**current_state, **updates}
        
        # Update metadata
        updated_state["timestamps"]["updated_at"] = datetime.now().astimezone().isoformat()
        updated_state["timestamps"]["last_heartbeat"] = datetime.now().astimezone().isoformat()
        
        # Write back
        f.seek(0)
        json.dump(updated_state, f, indent=2)
        f.truncate()
        
        fcntl.flock(f, fcntl.LOCK_UN)
    
    return updated_state

def validate_worker_state(worker_state):
    """
    Validate individual worker state consistency
    """
    validations = {
        "has_required_fields": all(field in worker_state for field in 
                                  ["status", "task", "spawned_at"]),
        "status_valid": worker_state["status"] in 
                       ["planned", "spawning", "active", "completed", "failed"],
        "metrics_consistent": worker_state["metrics"]["events_logged"] > 0 
                             if worker_state["status"] == "completed" else True,
        "outputs_present": bool(worker_state["outputs"]) 
                          if worker_state["status"] == "completed" else True
    }
    return all(validations.values()), validations

def recover_state(session_id):
    """
    Recover STATE.json from EVENTS.jsonl if corrupted
    """
    events_path = f"Docs/hive-mind/sessions/{session_id}/EVENTS.jsonl"
    
    # Rebuild state from events
    rebuilt_state = {
        "version": "2.0",
        "session_id": session_id,
        "coordination_status": {
            "workers_spawned": [],
            "workers_completed": []
        }
    }
    
    with open(events_path, 'r') as f:
        for line in f:
            event = json.loads(line)
            
            if event.get("type") == "session_created":
                rebuilt_state["created_at"] = event["timestamp"]
                
            elif event.get("type") == "worker_spawned":
                rebuilt_state["coordination_status"]["workers_spawned"].append(
                    event.get("agent")
                )
                
            elif event.get("type") == "worker_completed":
                rebuilt_state["coordination_status"]["workers_completed"].append(
                    event.get("agent")
                )
    
    return rebuilt_state

def check_worker_health(session_id):
    """
    Monitor worker health via heartbeat
    """
    state = read_state(session_id)
    current_time = datetime.now().astimezone()
    unhealthy_workers = []
    
    for worker_name, worker_state in state["worker_states"].items():
        if worker_state["status"] == "active":
            last_heartbeat = datetime.fromisoformat(worker_state["last_heartbeat"])
            time_since_heartbeat = (current_time - last_heartbeat).seconds
            
            if time_since_heartbeat > 300:  # 5 minutes timeout
                unhealthy_workers.append({
                    "worker": worker_name,
                    "last_seen": worker_state["last_heartbeat"],
                    "timeout_seconds": time_since_heartbeat
                })
    
    return unhealthy_workers

def deep_merge(dict1, dict2):
    """
    Deep merge two dictionaries
    """
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def read_state(session_id):
    """
    Read current STATE.json
    """
    state_path = f"Docs/hive-mind/sessions/{session_id}/STATE.json"
    with open(state_path, 'r') as f:
        return json.load(f)
