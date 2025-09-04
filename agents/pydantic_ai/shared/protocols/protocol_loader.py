#!/usr/bin/env python3
"""
Protocol Loader - Base classes for protocol implementations
"""

from typing import Dict, Any, List
from datetime import datetime
from pathlib import Path
import json


class ProtocolConfig:
    """Configuration for protocol implementations with canonical field names only

    Canonical field names:
    - agent_name: worker/agent identifier  
    - timeout: escalation / operation timeout seconds
    - retries: retry attempts for recoverable ops
    - prompt_text: original prompt input
    - session_id: session identifier
    - session_path: resolved session path (optional; can be derived)
    """

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        
        # Canonical names only - no backward compatibility
        self.session_id = self.config.get("session_id")
        self.session_path = self.config.get("session_path")
        self.agent_name = self.config.get("agent_name")
        self.timeout = self.config.get("timeout")
        self.retries = self.config.get("retries") 
        self.prompt_text = self.config.get("prompt_text")
        
        # Validate required fields
        if not self.agent_name:
            raise ValueError("ProtocolConfig requires 'agent_name' field")
        if not self.session_id:
            raise ValueError("ProtocolConfig requires 'session_id' field")


class BaseProtocol:
    """Base class for all protocol implementations"""

    def __init__(self, config: Dict[str, Any] = None):
        if isinstance(config, ProtocolConfig):
            self.config = config
        else:
            self.config = ProtocolConfig(config)
