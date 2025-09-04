#!/usr/bin/env python3
"""
Logging Protocol Implementation 
======================================
Unified logging protocol with atomic operations.
"""

from datetime import datetime
from typing import Dict, Any
from .protocol_loader import BaseProtocol, ProtocolConfig
from .session_management import SessionManagement


class LoggingProtocol(BaseProtocol):
    """Handles all logging operations with atomic guarantees"""

    def __init__(self, config: ProtocolConfig):
        super().__init__(config)
        self.log_buffer = []

    def log_event(
        self, event_type: str, details: Any, level: str = "INFO"
    ) -> Dict[str, Any]:
        """
        Atomic event logging to EVENTS.jsonl using append-safe operations
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        event = {
            "timestamp": timestamp,
            "level": level,
            "type": event_type,
            "agent": self.config.agent_name or "system",
            "details": details,
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

    def log_debug(
        self, message: str, details: Any, level: str = "DEBUG"
    ) -> Dict[str, Any]:
        """
        Debug logging to DEBUG.jsonl using append-safe operations
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        debug_entry = {
            "timestamp": timestamp,
            "level": level,
            "agent": self.config.agent_name or "system",
            "message": message,
            "details": details,
        }

        # Use unified append-safe method - NEVER overwrites
        if self.config.session_id:
            SessionManagement.append_to_debug(self.config.session_id, debug_entry)

        return debug_entry

    def log_error(self, message: str, details: Any) -> Dict[str, Any]:
        """Log error message using debug logging with ERROR level"""
        return self.log_debug(message, details, "ERROR")

    def log_warning(self, message: str, details: Any) -> Dict[str, Any]:
        """Log warning message using debug logging with WARNING level"""
        return self.log_debug(message, details, "WARNING")

    def log_backlog(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Log to BACKLOG.jsonl for deferred items using append-safe operations
        """
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        backlog_entry = {
            "timestamp": timestamp,
            "created_by": self.config.agent_name or "system",
            "item": item,
            "status": "pending",
            "priority": item.get("priority", "normal"),
        }

        # Use unified append-safe method - NEVER overwrites
        if self.config.session_id:
            SessionManagement.append_to_backlog(self.config.session_id, backlog_entry)

        return backlog_entry
