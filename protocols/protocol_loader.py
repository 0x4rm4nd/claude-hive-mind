#!/usr/bin/env python3
"""
Protocol Loader - Base classes for protocol implementations
"""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import json

class ProtocolConfig:
    """Configuration for protocol implementations"""
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.session_id = config.get("session_id") if config else None
        self.session_path = config.get("session_path") if config else None

class BaseProtocol:
    """Base class for all protocol implementations"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = ProtocolConfig(config)
        self.execution_log = []
    
    def log_execution(self, action: str, data: Any):
        """Log protocol execution events"""
        self.execution_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "data": data
        })
    
    def log_debug(self, message: str, level: str = "INFO", details: Any = None) -> None:
        """Append debug information to DEBUG.jsonl - ALWAYS APPEND, never overwrite"""
        if not self.config.session_path:
            return  # Silent fail if no session path available
        
        debug_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "agent": getattr(self, 'worker_name', 'protocol'),
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