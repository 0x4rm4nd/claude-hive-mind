#!/usr/bin/env python3
"""
Protocol Loader - Base classes for protocol implementations
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pathlib import Path
import json
from .config_validator import config_validator
from .session_management import SessionManagement
from .protocol_interface import (
    ProtocolInterface, 
    LoggingCapable, 
    SessionAware, 
    FileOperationCapable,
    ProtocolMetadata,
    dependency_container
)


class ProtocolConfig:
    """Configuration for protocol implementations with validation"""

    # Required fields for all protocols
    REQUIRED_FIELDS = ["session_id"]
    
    # Optional fields with defaults
    DEFAULT_VALUES = {
        "timeout": 3600,  # Within 1-86400 range
        "retries": 3,     # Within 0-10 range  
        "agent_name": "system",
        "session_path": None,
        "prompt_text": ""
    }

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._set_canonical_fields()  # Apply defaults first
        self._validate_config()       # Then validate  
        self._resolve_session_path()

    def _validate_config(self) -> None:
        """Validate configuration using comprehensive validation system"""
        
        # Create validation dict with actual field values after defaults applied
        validation_config = {
            "session_id": self.session_id,
            "agent_name": self.agent_name,
            "timeout": self.timeout,
            "retries": self.retries,
            "prompt_text": self.prompt_text,
            "session_path": self.session_path
        }
        
        # Use comprehensive validation
        validation_result = config_validator.validate_config(validation_config, "base_protocol")
        
        if not validation_result.is_valid:
            error_details = "; ".join(validation_result.errors)
            raise ValueError(f"Configuration validation failed: {error_details}")
        
        # CRITICAL: Fail hard on configuration warnings (unexpected fields)
        if validation_result.warnings:
            warnings_detail = "; ".join(validation_result.warnings)
            raise ValueError(f"Configuration validation warnings (strict mode): {warnings_detail}")

    def _set_canonical_fields(self) -> None:
        """Set canonical field values with defaults"""
        # Set canonical names with defaults
        for field, default_value in self.DEFAULT_VALUES.items():
            setattr(self, field, self.config.get(field, default_value))
        
        # Required fields (no defaults)
        for field in self.REQUIRED_FIELDS:
            setattr(self, field, self.config.get(field))
        
        # Handle backward compatibility mapping
        if not self.agent_name or self.agent_name == "system":
            self.agent_name = self.config.get("worker_type", "system")
    
    def _resolve_session_path(self) -> None:
        """Resolve session path from session_id if not provided"""
        if not self.session_path and self.session_id:
            self.session_path = SessionManagement.get_session_path(self.session_id)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            "session_id": self.session_id,
            "session_path": self.session_path,
            "agent_name": self.agent_name,
            "timeout": self.timeout,
            "retries": self.retries,
            "prompt_text": self.prompt_text
        }


class BaseProtocol(ProtocolInterface, LoggingCapable, SessionAware, FileOperationCapable):
    """
    Base class for all protocol implementations implementing standard interfaces.
    Provides dependency injection, fail-hard error handling, and unified logging capabilities.
    """
    
    # Protocol metadata
    _metadata = ProtocolMetadata(
        name="BaseProtocol",
        version="2.0.0", 
        description="Base protocol implementation with interface compliance",
        capabilities=["logging", "session_aware", "file_operations"]
    )

    def __init__(self, config: Dict[str, Any] = None):
        if isinstance(config, ProtocolConfig):
            self.config = config
        else:
            self.config = ProtocolConfig(config)
        
        self.execution_log = []
        self.dependencies = {}
        self._initialized = False
        self._status = {"healthy": True, "last_check": datetime.now().isoformat()}
        
        # Initialize with dependency injection
        self.initialize(self.config.to_dict())

    # ProtocolInterface implementation
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the protocol with configuration"""
        try:
            # Inject dependencies if available
            self._inject_dependencies()
            self._initialized = True
            self.log_event("protocol_initialized", {"config_keys": list(config.keys())})
            return True
        except Exception as e:
            # handle_error now raises exceptions (fail hard) - no return needed
            self.handle_error(e, {"operation": "initialization", "config": config})

    def validate_config(self, config: Dict[str, Any]) -> bool:
        """Validate protocol configuration"""
        try:
            # Use ProtocolConfig validation
            ProtocolConfig(config)
            return True
        except ValueError as e:
            raise ValueError(f"Protocol configuration validation failed: {str(e)}")

    def cleanup(self) -> None:
        """Cleanup protocol resources"""
        self.log_event("protocol_cleanup", {"execution_log_entries": len(self.execution_log)})
        self.execution_log.clear()
        self.dependencies.clear()
        self._initialized = False

    def get_status(self) -> Dict[str, Any]:
        """Get current protocol status"""
        self._status.update({
            "initialized": self._initialized,
            "execution_log_size": len(self.execution_log),
            "dependencies_loaded": len(self.dependencies),
            "last_check": datetime.now().isoformat()
        })
        return self._status

    def handle_error(self, error: Exception, context: Dict[str, Any]) -> bool:
        """Handle protocol errors - fail hard, no recovery"""
        
        # Log error before failing hard
        self.log_event("protocol_error", {
            "error": str(error),
            "error_type": type(error).__name__,
            "operation": context.get("operation", "unknown"),
            "protocol_name": self.__class__.__name__,
            "session_id": self.config.session_id,
            "context": context
        }, "ERROR")
        
        # CRITICAL: Fail hard - no recovery attempts
        raise error

    # LoggingCapable implementation
    def log_event(self, event_type: str, details: Any, level: str = "INFO") -> Dict[str, Any]:
        """Log an event to the session event stream"""
        timestamp = datetime.now().isoformat()
        
        event = {
            "timestamp": timestamp,
            "level": level,
            "type": event_type,
            "agent": self.config.agent_name,
            "details": details,
        }
        
        # Log to execution log
        self.execution_log.append(event)
        
        # Log to session if available
        if self.config.session_id:
            SessionManagement.append_to_events(self.config.session_id, event)
        
        return event

    def log_debug(self, message: str, details: Any = None, level: str = "DEBUG") -> Dict[str, Any]:
        """Log debug information to session debug stream"""
        timestamp = datetime.now().isoformat()
        
        debug_entry = {
            "timestamp": timestamp,
            "level": level,
            "agent": self.config.agent_name,
            "message": message,
            "details": details,
        }
        
        # Log to session if available
        if self.config.session_id:
            SessionManagement.append_to_debug(self.config.session_id, debug_entry)
        
        return debug_entry

    # SessionAware implementation
    @property
    def session_id(self) -> Optional[str]:
        """Get current session identifier"""
        return self.config.session_id

    @property
    def session_path(self) -> Optional[str]:
        """Get current session directory path"""
        return self.config.session_path

    def ensure_session_validity(self) -> bool:
        """Ensure session exists and is valid - fail hard if not"""
        if not self.config.session_id:
            raise ValueError("Session ID is required for session-aware protocols")
        
        from .session_management import SessionManagement
        return SessionManagement.ensure_session_exists(self.config.session_id)

    # FileOperationCapable implementation
    def create_file(self, file_path: str, content: Any, file_type: str = "text") -> bool:
        """Create a file with atomic write operations"""
        try:
            file_path_obj = Path(file_path)
            
            # Ensure parent directory exists
            self.ensure_directory_exists(str(file_path_obj.parent))
            
            if file_type == "json":
                content_str = json.dumps(content, indent=2) if not isinstance(content, str) else content
            else:
                content_str = str(content)
            
            # Atomic write
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_str)
            
            self.log_event("file_created", {"path": file_path, "type": file_type})
            return True
            
        except Exception as e:
            # handle_error now raises exceptions (fail hard) - no return needed  
            self.handle_error(e, {"operation": "create_file", "path": file_path, "type": file_type})

    def append_to_file(self, file_path: str, content: Any) -> bool:
        """Append content to file with atomic operations"""
        try:
            content_str = str(content) if not isinstance(content, str) else content
            
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(content_str)
            
            self.log_event("file_appended", {"path": file_path})
            return True
            
        except Exception as e:
            # handle_error now raises exceptions (fail hard) - no return needed
            self.handle_error(e, {"operation": "append_to_file", "path": file_path})

    def ensure_directory_exists(self, directory_path: str) -> bool:
        """Ensure directory exists, creating if necessary"""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            # handle_error now raises exceptions (fail hard) - no return needed
            self.handle_error(e, {"operation": "ensure_directory", "path": directory_path})

    # Private helper methods
    def _inject_dependencies(self) -> None:
        """Inject dependencies from container"""
        try:
            # Inject common dependencies
            dependency_map = {
                "session_manager": "session_management",
                "logger": "logging_protocol"
            }
            
            for attr_name, dep_name in dependency_map.items():
                try:
                    dependency = dependency_container.get(dep_name)
                    self.dependencies[attr_name] = dependency
                    setattr(self, attr_name, dependency)
                except ValueError:
                    # Dependency not available, continue without it
                    continue
                    
        except Exception as e:
            # Log but don't fail initialization for dependency injection issues
            self.log_debug("Dependency injection failed", {"error": str(e)}, "WARNING")


    def log_execution(self, action: str, status_or_data: Any = None, data: Any = None):
        """Legacy method for backward compatibility"""
        if data is None:
            status = None
            payload = status_or_data
        else:
            status = status_or_data
            payload = data
            
        self.log_event(f"execution_{action}", {
            "status": status,
            "data": payload
        })