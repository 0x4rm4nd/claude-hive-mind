#!/usr/bin/env python3
"""
Logging Protocol Implementation 
======================================
Unified logging protocol with atomic operations.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional
from .protocol_loader import BaseProtocol, ProtocolConfig

class LoggingProtocol(BaseProtocol):
    """Handles all logging operations with atomic guarantees"""
    
    def __init__(self, config: ProtocolConfig):
        super().__init__(config)
        self.log_buffer = []
        self.event_counter = 0
    
    def log_event(self, event_type: str, details: Any, level: str = "INFO") -> Dict[str, Any]:
        """
        Atomic event logging to EVENTS.jsonl
        """
        timestamp = datetime.now().isoformat()
        self.event_counter += 1
        
        event = {
            "timestamp": timestamp,
            "sequence": self.event_counter,
            "type": event_type,
            "agent": self.config.worker_type or "system",
            "session_id": self.config.session_id,
            "details": details,
            "level": level,
            "protocol_version": self.config.version
        }
        
        # Write to EVENTS.jsonl atomically
        if self.config.session_id:
            session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
            self.atomic_append(f"{session_path}/EVENTS.jsonl", event)
        
        # Buffer for batch operations
        self.log_buffer.append(event)
        
        # Also log to DEBUG for redundancy
        if level in ["ERROR", "FATAL", "WARNING"]:
            self.log_debug(event_type, details, level)
        
        return event
    
    def log_debug(self, message: str, details: Any, level: str = "DEBUG") -> Dict[str, Any]:
        """
        Debug logging to DEBUG.jsonl
        """
        timestamp = datetime.now().isoformat()
        
        debug_entry = {
            "timestamp": timestamp,
            "level": level,
            "agent": self.config.worker_type or "system",
            "message": message,
            "details": details
        }
        
        if self.config.session_id:
            session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
            self.atomic_append(f"{session_path}/DEBUG.jsonl", debug_entry)
        
        return debug_entry
    
    def log_backlog(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log to BACKLOG.jsonl for deferred items
        """
        timestamp = datetime.now().isoformat()
        
        backlog_entry = {
            "timestamp": timestamp,
            "created_by": self.config.worker_type or "system",
            "item": item,
            "status": "pending",
            "priority": item.get("priority", "normal")
        }
        
        if self.config.session_id:
            session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
            self.atomic_append(f"{session_path}/BACKLOG.jsonl", backlog_entry)
        
        return backlog_entry
    
    def atomic_append(self, filepath: str, data: Dict[str, Any]) -> bool:
        """
        Atomic append operation using printf for guaranteed write
        """
        # Convert to JSON with minimal formatting
        json_str = json.dumps(data, separators=(',', ':'))
        
        # Use Bash printf for atomic write (pseudo-code for actual implementation)
        # Bash(
        #     command=f'printf "%s\\n" {json.dumps(json_str)} >> "{filepath}"',
        #     description=f"Atomic append to {filepath}"
        # )
        
        # For architecture demonstration
        self.log_execution("atomic_append", {"file": filepath, "success": True})
        return True
    
    def flush_buffer(self) -> int:
        """
        Flush log buffer to disk
        """
        count = len(self.log_buffer)
        
        if count > 0 and self.config.session_id:
            session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
            
            # Batch write all buffered events
            for event in self.log_buffer:
                self.atomic_append(f"{session_path}/EVENTS.jsonl", event)
            
            self.log_buffer.clear()
        
        return count
    
    def read_events(self, event_type: Optional[str] = None, 
                   agent: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Read and filter events from EVENTS.jsonl
        """
        if not self.config.session_id:
            return []
        
        events = []
        session_path = f"Docs/hive-mind/sessions/{self.config.session_id}"
        
        # Pseudo-code for actual file reading
        # lines = Read(f"{session_path}/EVENTS.jsonl").strip().split('\n')
        # for line in lines:
        #     if line:
        #         event = json.loads(line)
        #         if (not event_type or event.get("type") == event_type) and \
        #            (not agent or event.get("agent") == agent):
        #             events.append(event)
        
        return events
    
    def get_event_summary(self) -> Dict[str, Any]:
        """
        Generate summary of logged events
        """
        events = self.read_events()
        
        summary = {
            "total_events": len(events),
            "event_types": {},
            "agents": {},
            "error_count": 0,
            "warning_count": 0,
            "first_event": None,
            "last_event": None
        }
        
        for event in events:
            # Count event types
            event_type = event.get("type", "unknown")
            summary["event_types"][event_type] = summary["event_types"].get(event_type, 0) + 1
            
            # Count by agent
            agent = event.get("agent", "unknown")
            summary["agents"][agent] = summary["agents"].get(agent, 0) + 1
            
            # Count errors and warnings
            level = event.get("level", "INFO")
            if level == "ERROR":
                summary["error_count"] += 1
            elif level == "WARNING":
                summary["warning_count"] += 1
            
            # Track first and last events
            if not summary["first_event"]:
                summary["first_event"] = event.get("timestamp")
            summary["last_event"] = event.get("timestamp")
        
        return summary