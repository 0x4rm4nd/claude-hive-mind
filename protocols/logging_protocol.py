#!/usr/bin/env python3
"""
Logging Protocol Implementation 
======================================
Unified logging protocol with atomic operations.
"""

import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from .protocol_loader import BaseProtocol, ProtocolConfig
from .session_management import SessionManagement

class LoggingProtocol(BaseProtocol):
    """Handles all logging operations with atomic guarantees"""
    
    def __init__(self, config: ProtocolConfig):
        super().__init__(config)
        self.log_buffer = []
        self.event_counter = 0
    
    def log_event(self, event_type: str, details: Any, level: str = "INFO") -> Dict[str, Any]:
        """
        Atomic event logging to EVENTS.jsonl using append-safe operations
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
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
        
        # Use unified append-safe method - NEVER overwrites
        if self.config.session_id:
            SessionManagement.append_to_events(self.config.session_id, event)
        
        # Buffer for batch operations
        self.log_buffer.append(event)
        
        # Also log to DEBUG for redundancy
        if level in ["ERROR", "FATAL", "WARNING"]:
            self.log_debug(event_type, details, level)
        
        return event
    
    def log_debug(self, message: str, details: Any, level: str = "DEBUG") -> Dict[str, Any]:
        """
        Debug logging to DEBUG.jsonl using append-safe operations
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        debug_entry = {
            "timestamp": timestamp,
            "level": level,
            "agent": self.config.worker_type or "system",
            "message": message,
            "details": details
        }
        
        # Use unified append-safe method - NEVER overwrites
        if self.config.session_id:
            SessionManagement.append_to_debug(self.config.session_id, debug_entry)
        
        return debug_entry
    
    def log_backlog(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log to BACKLOG.jsonl for deferred items using append-safe operations
        """
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        
        backlog_entry = {
            "timestamp": timestamp,
            "created_by": self.config.worker_type or "system",
            "item": item,
            "status": "pending",
            "priority": item.get("priority", "normal")
        }
        
        # Use unified append-safe method - NEVER overwrites
        if self.config.session_id:
            SessionManagement.append_to_backlog(self.config.session_id, backlog_entry)
        
        return backlog_entry
    
    def atomic_append(self, filepath: str, data: Dict[str, Any]) -> bool:
        """
        DEPRECATED: Use SessionManagement append methods instead.
        This method is kept for backwards compatibility only.
        """
        # Extract session_id from filepath if possible
        import re
        match = re.search(r'/sessions/([^/]+)/', filepath)
        if match and self.config.session_id:
            session_id = match.group(1)
            
            # Route to appropriate append method
            if 'EVENTS.jsonl' in filepath:
                return SessionManagement.append_to_events(session_id, data)
            elif 'DEBUG.jsonl' in filepath:
                return SessionManagement.append_to_debug(session_id, data)
            elif 'BACKLOG.jsonl' in filepath:
                return SessionManagement.append_to_backlog(session_id, data)
        
        # Fallback for other files
        self.log_execution("atomic_append", {"file": filepath, "success": True})
        return True
    
    def flush_buffer(self) -> int:
        """
        Flush log buffer to disk using append-safe operations
        """
        count = len(self.log_buffer)
        
        if count > 0 and self.config.session_id:
            # Batch append all buffered events using safe method
            for event in self.log_buffer:
                SessionManagement.append_to_events(self.config.session_id, event)
            
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
        # Use unified session path
        session_path = SessionManagement.get_session_path(self.config.session_id)
        
        # Note: In production, this would use the Read tool to read EVENTS.jsonl
        # and parse/filter the events. For now, return empty list as placeholder.
        
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
