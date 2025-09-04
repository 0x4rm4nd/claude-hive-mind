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
        self.timeout = self.config.get("timeout")
        self.retries = self.config.get("retries")
        self.prompt_text = self.config.get("prompt_text")

        # Backward-compatibility aliases (mapped to canonical if missing)
        if not self.agent_name:
            self.agent_name = self.config.get("worker_type")
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
