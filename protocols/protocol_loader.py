#!/usr/bin/env python3
"""
Protocol Loader - Base classes for protocol implementations
"""

from typing import Dict, Any, List
from datetime import datetime

class ProtocolConfig:
    """Configuration for protocol implementations"""
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}

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