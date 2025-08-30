#!/usr/bin/env python3
"""
Session Protocol Implementation 
======================================
Manages session lifecycle and state.
"""

import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, List
from .protocol_loader import BaseProtocol, ProtocolConfig
from .session_management import SessionManagement

class SessionProtocol(BaseProtocol):
    """Handles session creation, management, and state"""
    
    def create_session(self, task: str, complexity_level: int) -> Dict[str, Any]:
        """
        Create a new session with complete scaffolding
        """
        # Generate session ID
        task_slug = re.sub(r'[^a-zA-Z0-9]+', '-', task.lower())[:50]
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
        session_id = f"{timestamp}-{task_slug}"
        
        self.config.session_id = session_id
        session_path = f"Docs/hive-mind/sessions/{session_id}"
        
        # Create directory structure atomically
        # Bash(command=f"""
        #     mkdir -p '{session_path}/workers/json' \
        #              '{session_path}/workers/prompts' \
        #              '{session_path}/workers/decisions' && \
        #     touch '{session_path}/EVENTS.jsonl' \
        #           '{session_path}/DEBUG.jsonl' \
        #           '{session_path}/BACKLOG.jsonl'
        # """, description="Create session structure")
        
        # Initialize state
        state = {
            "session_id": session_id,
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "task": task,
            "complexity_level": complexity_level,
            "coordinator": self.config.worker_type or "queen-orchestrator",
            "status": "initializing",
            "coordination_status": {
                "phase": "planning",
                "workers_spawned": [],
                "workers_completed": [],
                "workers_pending": [],
                "workers_failed": [],
                "synthesis_ready": False
            },
            "worker_configs": {},
            "metrics": {
                "start_time": datetime.now().isoformat(),
                "events_logged": 0,
                "workers_total": 0,
                "completion_percentage": 0
            }
        }
        
        # Write initial state
        self.write_state(state)
        
        # Create session summary
        self.create_session_summary(session_id, task, complexity_level)
        
        self.log_execution("create_session", {
            "session_id": session_id,
            "status": "created"
        })
        
        return {
            "session_id": session_id,
            "session_path": session_path,
            "initial_state": state
        }
    
    def read_state(self) -> Dict[str, Any]:
        """Read current session state"""
        if not self.config.session_id:
            self.log_debug(
                "read_state failed - Session ID not configured",
                "ERROR",
                details={
                    "operation": "read_state",
                    "config_state": str(self.config.__dict__ if hasattr(self.config, '__dict__') else 'N/A'),
                    "error": "Session ID not configured"
                }
            )
            raise ValueError("Session ID not configured")
        
        session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
        
        # Pseudo-code for actual file reading
        # return json.loads(Read(f"{session_path}/STATE.json"))
        
        # Placeholder for demonstration
        return {
            "session_id": self.config.session_id,
            "status": "active",
            "coordination_status": {}
        }
    
    def write_state(self, state: Dict[str, Any]) -> bool:
        """Write session state atomically"""
        if not self.config.session_id:
            self.log_debug(
                "write_state failed - Session ID not configured",
                "ERROR",
                details={
                    "operation": "write_state",
                    "state_to_write": state,
                    "config_state": str(self.config.__dict__ if hasattr(self.config, '__dict__') else 'N/A'),
                    "error": "Session ID not configured"
                }
            )
            raise ValueError("Session ID not configured")
        
        state["last_updated"] = datetime.now().isoformat()
        session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
        
        # Write(f"{session_path}/STATE.json", json.dumps(state, indent=2))
        
        self.log_execution("write_state", {"updated": True})
        return True
    
    def update_state(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update session state with partial changes"""
        current_state = self.read_state()
        
        # Deep merge updates into current state
        for key, value in updates.items():
            if isinstance(value, dict) and key in current_state and isinstance(current_state[key], dict):
                current_state[key].update(value)
            else:
                current_state[key] = value
        
        self.write_state(current_state)
        return current_state
    
    def update_worker_status(self, worker_type: str, status: str, 
                           metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """Update worker status in session state"""
        state = self.read_state()
        coordination_status = state.get("coordination_status", {})
        
        # Update worker lists based on status
        if status == "spawned":
            if worker_type not in coordination_status.get("workers_spawned", []):
                coordination_status.setdefault("workers_spawned", []).append(worker_type)
            if worker_type in coordination_status.get("workers_pending", []):
                coordination_status["workers_pending"].remove(worker_type)
                
        elif status == "completed":
            if worker_type not in coordination_status.get("workers_completed", []):
                coordination_status.setdefault("workers_completed", []).append(worker_type)
            if worker_type in coordination_status.get("workers_spawned", []):
                coordination_status["workers_spawned"].remove(worker_type)
                
        elif status == "failed":
            if worker_type not in coordination_status.get("workers_failed", []):
                coordination_status.setdefault("workers_failed", []).append(worker_type)
            if worker_type in coordination_status.get("workers_spawned", []):
                coordination_status["workers_spawned"].remove(worker_type)
        
        # Update metrics
        metrics = state.get("metrics", {})
        total_workers = len(set(
            coordination_status.get("workers_spawned", []) +
            coordination_status.get("workers_completed", []) +
            coordination_status.get("workers_failed", [])
        ))
        
        if total_workers > 0:
            completed = len(coordination_status.get("workers_completed", []))
            metrics["completion_percentage"] = (completed / total_workers) * 100
        
        # Apply updates
        state["coordination_status"] = coordination_status
        state["metrics"] = metrics
        
        if metadata:
            state.setdefault("worker_metadata", {})[worker_type] = metadata
        
        self.write_state(state)
        
        return state
    
    def create_session_summary(self, session_id: str, task: str, complexity: int) -> None:
        """Create SESSION.md summary file"""
        summary_content = f"""# Session: {session_id}

## Task
{task}

## Metadata
- **Created**: {datetime.now().isoformat()}
- **Complexity Level**: {complexity}/4
- **Coordinator**: {self.config.worker_type or 'queen-orchestrator'}
- **Protocol Version**: {self.config.version}

## Workers
*Pending assignment*

## Progress
- [ ] Session initialized
- [ ] Workers planned
- [ ] Workers spawned
- [ ] Analysis in progress
- [ ] Synthesis ready
- [ ] Session complete

## Notes
*Session coordination in progress...*
"""
        
        session_path = f"Docs/hive-mind/sessions/{session_id}"
        # Write(f"{session_path}/SESSION.md", summary_content)
    
    def validate_session_structure(self) -> Dict[str, bool]:
        """Validate session directory structure"""
        if not self.config.session_id:
            return {"valid": False, "error": "No session ID"}
        
        session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
        
        validation = {
            "directories": {
                "workers": False,
                "workers/json": False,
                "workers/prompts": False,
                "workers/decisions": False
            },
            "files": {
                "STATE.json": False,
                "EVENTS.jsonl": False,
                "DEBUG.jsonl": False,
                "BACKLOG.jsonl": False,
                "SESSION.md": False
            }
        }
        
        # Check each required path (pseudo-code)
        # for dir_name in validation["directories"]:
        #     validation["directories"][dir_name] = exists(f"{session_path}/{dir_name}")
        # for file_name in validation["files"]:
        #     validation["files"][file_name] = exists(f"{session_path}/{file_name}")
        
        validation["valid"] = all(
            list(validation["directories"].values()) + 
            list(validation["files"].values())
        )
        
        return validation
    
    def get_session_metrics(self) -> Dict[str, Any]:
        """Get comprehensive session metrics"""
        state = self.read_state()
        
        metrics = state.get("metrics", {})
        coordination = state.get("coordination_status", {})
        
        # Calculate duration
        if "start_time" in metrics:
            start = datetime.fromisoformat(metrics["start_time"])
            duration = (datetime.now() - start).total_seconds()
            metrics["duration_seconds"] = duration
            metrics["duration_formatted"] = f"{int(duration//60)}m {int(duration%60)}s"
        
        # Worker statistics
        metrics["workers"] = {
            "total": len(set(
                coordination.get("workers_spawned", []) +
                coordination.get("workers_completed", []) +
                coordination.get("workers_failed", [])
            )),
            "active": len(coordination.get("workers_spawned", [])),
            "completed": len(coordination.get("workers_completed", [])),
            "failed": len(coordination.get("workers_failed", []))
        }
        
        return metrics
    
    def close_session(self) -> Dict[str, Any]:
        """Close and finalize session"""
        state = self.read_state()
        
        # Update final status
        state["status"] = "completed"
        state["completed_at"] = datetime.now().isoformat()
        
        # Calculate final metrics
        metrics = self.get_session_metrics()
        state["final_metrics"] = metrics
        
        # Mark synthesis ready if all workers complete
        coordination = state.get("coordination_status", {})
        if not coordination.get("workers_spawned") and not coordination.get("workers_pending"):
            coordination["synthesis_ready"] = True
            coordination["phase"] = "synthesis_complete"
        
        state["coordination_status"] = coordination
        
        self.write_state(state)
        
        self.log_execution("close_session", {
            "session_id": self.config.session_id,
            "status": "closed",
            "metrics": metrics
        })
        
        return state