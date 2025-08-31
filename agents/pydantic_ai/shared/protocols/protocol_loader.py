#!/usr/bin/env python3
"""
Protocol Loader - Base classes for protocol implementations
"""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import json

class ProtocolConfig:
    """Configuration for protocol implementations (template-aligned fields)

    Canonical field names per templates:
    - agent_name: worker/agent identifier (was worker_type)
    - protocol_version: protocol version string (was version)
    - timeout: escalation / operation timeout seconds (was escalation_timeout)
    - retries: retry attempts for recoverable ops (was retry_attempts)
    - prompt_text: original prompt input (was initial_prompt)
    - session_id: session identifier
    - session_path: resolved session path (optional; can be derived)
    """
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        # Canonical names
        self.session_id = self.config.get("session_id")
        self.session_path = self.config.get("session_path")
        self.agent_name = self.config.get("agent_name")
        self.protocol_version = self.config.get("protocol_version")
        self.timeout = self.config.get("timeout")
        self.retries = self.config.get("retries")
        self.prompt_text = self.config.get("prompt_text")

        # Backward-compatibility aliases (mapped to canonical if missing)
        if not self.agent_name:
            self.agent_name = self.config.get("worker_type")
        if not self.protocol_version:
            self.protocol_version = self.config.get("version")
        if self.timeout is None:
            self.timeout = self.config.get("escalation_timeout")
        if self.retries is None:
            self.retries = self.config.get("retry_attempts")
        if not self.prompt_text:
            self.prompt_text = self.config.get("initial_prompt")

class BaseProtocol:
    """Base class for all protocol implementations"""
    
    def __init__(self, config: Dict[str, Any] = None):
        if isinstance(config, ProtocolConfig):
            self.config = config
        else:
            self.config = ProtocolConfig(config)
        self.execution_log = []
    
    def log_execution(self, action: str, status_or_data: Any = None, data: Any = None):
        """Log protocol execution events
        Accepts either (action, data) or (action, status, data) for compatibility.
        """
        if data is None:
            status = None
            payload = status_or_data
        else:
            status = status_or_data
            payload = data
        entry = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "action": action,
            "data": payload
        }
        if status is not None:
            entry["status"] = status
        self.execution_log.append(entry)
    
    def log_debug(self, message: str, level: str = "INFO", details: Any = None) -> None:
        """Append debug information to DEBUG.jsonl - ALWAYS APPEND, never overwrite"""
        # Try to resolve session_path from session_id if not provided
        if not self.config.session_path and getattr(self.config, "session_id", None):
            try:
                from .session_management import SessionManagement  # local import to avoid cycles
                self.config.session_path = SessionManagement.get_session_path(self.config.session_id)
            except Exception:
                pass
        if not self.config.session_path:
            return  # Silent fail if no session path available
        
        debug_entry = {
            "timestamp": datetime.now().astimezone().isoformat(),
            "level": level,
            "agent": getattr(self.config, 'agent_name', None) or getattr(self, 'worker_name', 'protocol'),
            "message": message,
            "details": details
        }
        
        # CRITICAL: Append mode to prevent overwriting + ensure file exists
        try:
            debug_file = Path(self.config.session_path) / "DEBUG.jsonl"
            if not debug_file.exists():
                debug_file.touch()  # Create if missing
            
            # ALWAYS append, never overwrite
            with debug_file.open('a', encoding='utf-8') as f:
                f.write(json.dumps(debug_entry, ensure_ascii=False) + '\n')
        except Exception:
            # Silent fail for debug logging to prevent cascading failures
            pass
