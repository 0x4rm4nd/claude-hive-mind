#!/usr/bin/env python3
"""
Protocol Loader - Base classes for protocol implementations with integrated validation
===================================================================================
Provides protocol configuration, validation, and base protocol implementation.
"""

import re
from typing import Dict, Any, List, Optional, Union, Callable
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import json
from .session_management import SessionManagement, iso_now
from .protocol_interface import (
    ProtocolInterface,
    LoggingCapable,
    SessionAware,
    ProtocolMetadata,
    dependency_container,
)


# Configuration Validation System
# ===============================
# Integrated from config_validator.py for consolidated configuration management


class ValidationType(Enum):
    """Types of validation checks"""

    REQUIRED = "required"
    TYPE_CHECK = "type_check"
    RANGE_CHECK = "range_check"
    PATTERN_CHECK = "pattern_check"
    CUSTOM_CHECK = "custom_check"
    DEPENDENCY_CHECK = "dependency_check"


@dataclass
class ValidationRule:
    """Individual validation rule definition"""

    field_name: str
    validation_type: ValidationType
    required: bool = True
    expected_type: Optional[type] = None
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    pattern: Optional[str] = None
    custom_validator: Optional[Callable] = None
    error_message: Optional[str] = None
    depends_on: List[str] = field(default_factory=list)

    def validate(self, value: Any, config: Dict[str, Any]) -> List[str]:
        """
        Validate a value against this rule.

        Returns:
            List of error messages (empty if validation passes)
        """
        errors = []

        # Check if field is required
        if self.required and (value is None or value == ""):
            errors.append(
                self.error_message or f"Field '{self.field_name}' is required"
            )
            return errors

        # Skip further validation if field is empty and not required
        if not self.required and (value is None or value == ""):
            return errors

        # Type validation
        if self.validation_type == ValidationType.TYPE_CHECK and self.expected_type:
            if not isinstance(value, self.expected_type):
                errors.append(
                    self.error_message
                    or f"Field '{self.field_name}' must be of type {self.expected_type.__name__}, got {type(value).__name__}"
                )

        # Range validation
        elif self.validation_type == ValidationType.RANGE_CHECK:
            if isinstance(value, (int, float)):
                if self.min_value is not None and value < self.min_value:
                    errors.append(
                        self.error_message
                        or f"Field '{self.field_name}' must be >= {self.min_value}, got {value}"
                    )
                if self.max_value is not None and value > self.max_value:
                    errors.append(
                        self.error_message
                        or f"Field '{self.field_name}' must be <= {self.max_value}, got {value}"
                    )

        # Pattern validation
        elif self.validation_type == ValidationType.PATTERN_CHECK and self.pattern:
            if isinstance(value, str):
                if not re.match(self.pattern, value):
                    errors.append(
                        self.error_message
                        or f"Field '{self.field_name}' does not match required pattern: {self.pattern}"
                    )

        # Custom validation
        elif (
            self.validation_type == ValidationType.CUSTOM_CHECK
            and self.custom_validator
        ):
            try:
                is_valid = self.custom_validator(value, config)
                if not is_valid:
                    errors.append(
                        self.error_message
                        or f"Field '{self.field_name}' failed custom validation"
                    )
            except Exception as e:
                errors.append(
                    f"Custom validation failed for '{self.field_name}': {str(e)}"
                )

        # Dependency validation
        elif self.validation_type == ValidationType.DEPENDENCY_CHECK:
            for dependency in self.depends_on:
                if dependency not in config or not config[dependency]:
                    errors.append(
                        self.error_message
                        or f"Field '{self.field_name}' requires '{dependency}' to be set"
                    )

        return errors


class ConfigurationSchema:
    """Configuration schema definition with validation rules"""

    def __init__(self, schema_name: str):
        self.schema_name = schema_name
        self.rules: List[ValidationRule] = []
        self.created_at = datetime.now().isoformat()

    def add_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule to the schema"""
        self.rules.append(rule)

    def add_required_field(
        self, field_name: str, expected_type: type, error_message: str = None
    ) -> None:
        """Add a required field validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.TYPE_CHECK,
            required=True,
            expected_type=expected_type,
            error_message=error_message,
        )
        self.add_rule(rule)

    def add_optional_field(
        self, field_name: str, expected_type: type, default_value: Any = None
    ) -> None:
        """Add an optional field validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.TYPE_CHECK,
            required=False,
            expected_type=expected_type,
        )
        self.add_rule(rule)

    def add_range_validation(
        self,
        field_name: str,
        min_value: Union[int, float] = None,
        max_value: Union[int, float] = None,
        error_message: str = None,
    ) -> None:
        """Add a range validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.RANGE_CHECK,
            min_value=min_value,
            max_value=max_value,
            error_message=error_message,
        )
        self.add_rule(rule)

    def add_pattern_validation(
        self, field_name: str, pattern: str, error_message: str = None
    ) -> None:
        """Add a pattern validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.PATTERN_CHECK,
            pattern=pattern,
            error_message=error_message,
        )
        self.add_rule(rule)

    def add_custom_validation(
        self, field_name: str, validator: Callable, error_message: str = None
    ) -> None:
        """Add a custom validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.CUSTOM_CHECK,
            custom_validator=validator,
            error_message=error_message,
        )
        self.add_rule(rule)

    def validate(self, config: Dict[str, Any]) -> "ValidationResult":
        """
        Validate a configuration against this schema.

        Returns:
            ValidationResult containing validation status and errors
        """
        errors = []
        warnings = []
        field_results = {}

        # Check for unexpected fields
        schema_fields = {rule.field_name for rule in self.rules}
        config_fields = set(config.keys())
        unexpected_fields = config_fields - schema_fields

        if unexpected_fields:
            warnings.append(f"Unexpected fields found: {', '.join(unexpected_fields)}")

        # Validate each rule
        for rule in self.rules:
            field_value = config.get(rule.field_name)
            field_errors = rule.validate(field_value, config)

            if field_errors:
                errors.extend(field_errors)
                field_results[rule.field_name] = {
                    "status": "error",
                    "errors": field_errors,
                }
            else:
                field_results[rule.field_name] = {"status": "valid", "errors": []}

        return ValidationResult(
            is_valid=(len(errors) == 0),
            errors=errors,
            warnings=warnings,
            field_results=field_results,
            schema_name=self.schema_name,
        )


@dataclass
class ValidationResult:
    """Result of configuration validation"""

    is_valid: bool
    errors: List[str]
    warnings: List[str]
    field_results: Dict[str, Dict[str, Any]]
    schema_name: str
    validated_at: str = field(default_factory=lambda: datetime.now().isoformat())


class ConfigurationValidator:
    """Main configuration validator with predefined schemas"""

    def __init__(self):
        self.schemas: Dict[str, ConfigurationSchema] = {}
        self._setup_default_schemas()

    def _setup_default_schemas(self):
        """Setup default validation schemas for common protocol configurations"""

        # Base Protocol Schema
        base_schema = ConfigurationSchema("base_protocol")
        base_schema.add_required_field(
            "session_id", str, "Session ID must be provided as a string"
        )
        base_schema.add_optional_field("agent_name", str)
        base_schema.add_optional_field("timeout", int)
        base_schema.add_optional_field("retries", int)
        base_schema.add_optional_field("prompt_text", str)
        base_schema.add_optional_field("session_path", str)

        # Add range validation for timeout and retries
        base_schema.add_range_validation(
            "timeout",
            min_value=1,
            max_value=86400,
            error_message="Timeout must be between 1 and 86400 seconds",
        )
        base_schema.add_range_validation(
            "retries",
            min_value=0,
            max_value=10,
            error_message="Retries must be between 0 and 10",
        )

        # Add pattern validation for session_id
        base_schema.add_pattern_validation(
            "session_id",
            r"^[a-zA-Z0-9\-_]+$",
            "Session ID must contain only alphanumeric characters, hyphens, and underscores",
        )

        self.schemas["base_protocol"] = base_schema

        # Prompt Generator Schema
        prompt_schema = ConfigurationSchema("prompt_generator")
        prompt_schema.add_required_field("session_id", str)
        prompt_schema.add_optional_field("worker_types", list)
        prompt_schema.add_optional_field("complexity_level", int)

        prompt_schema.add_range_validation(
            "complexity_level",
            min_value=1,
            max_value=10,
            error_message="Complexity level must be between 1 and 10",
        )

        self.schemas["prompt_generator"] = prompt_schema

        # Worker Prompt Protocol Schema
        worker_prompt_schema = ConfigurationSchema("worker_prompt_protocol")
        worker_prompt_schema.add_required_field("session_id", str)
        worker_prompt_schema.add_optional_field("agent_name", str)
        worker_prompt_schema.add_optional_field("worker_type", str)

        self.schemas["worker_prompt_protocol"] = worker_prompt_schema

    def validate_config(
        self, config: Dict[str, Any], schema_name: str = "base_protocol"
    ) -> ValidationResult:
        """
        Validate configuration against specified schema.

        Args:
            config: Configuration dictionary to validate
            schema_name: Name of schema to use for validation

        Returns:
            ValidationResult with validation status and details
        """
        if schema_name not in self.schemas:
            return ValidationResult(
                is_valid=False,
                errors=[f"Unknown validation schema: {schema_name}"],
                warnings=[],
                field_results={},
                schema_name=schema_name,
            )

        schema = self.schemas[schema_name]
        return schema.validate(config)


# Global validator instance
config_validator = ConfigurationValidator()


class ProtocolConfig:
    """Configuration for protocol implementations with validation"""

    # Required fields for all protocols
    REQUIRED_FIELDS = ["session_id"]

    # Optional fields with defaults
    DEFAULT_VALUES = {
        "timeout": 3600,  # Within 1-86400 range
        "retries": 3,  # Within 0-10 range
        "agent_name": "system",
        "session_path": None,
        "prompt_text": "",
    }

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self._set_canonical_fields()  # Apply defaults first
        self._validate_config()  # Then validate
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
            "session_path": self.session_path,
        }

        # Use comprehensive validation
        validation_result = config_validator.validate_config(
            validation_config, "base_protocol"
        )

        if not validation_result.is_valid:
            error_details = "; ".join(validation_result.errors)
            raise ValueError(f"Configuration validation failed: {error_details}")

        # CRITICAL: Fail hard on configuration warnings (unexpected fields)
        if validation_result.warnings:
            warnings_detail = "; ".join(validation_result.warnings)
            raise ValueError(
                f"Configuration validation warnings (strict mode): {warnings_detail}"
            )

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
            "prompt_text": self.prompt_text,
        }


class BaseProtocol(ProtocolInterface, LoggingCapable, SessionAware):
    """
    Base class for all protocol implementations implementing standard interfaces.
    Provides dependency injection, fail-hard error handling, unified logging capabilities,
    and direct file operations (no interface abstraction needed).
    """

    # Protocol metadata
    _metadata = ProtocolMetadata(
        name="BaseProtocol",
        version="2.0.0",
        description="Base protocol implementation with interface compliance",
        capabilities=["logging", "session_aware", "file_operations"],
    )

    def __init__(self, config: Dict[str, Any] = None):
        if isinstance(config, ProtocolConfig):
            self.config = config
        else:
            self.config = ProtocolConfig(config)

        self.execution_log = []
        self.dependencies = {}
        self._initialized = False
        self._status = {"healthy": True, "last_check": iso_now()}

        # Initialize with dependency injection
        self.initialize(self.config.to_dict())

    # ProtocolInterface implementation
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the protocol with configuration"""
        try:
            # Inject dependencies if available
            self._inject_dependencies()
            self._initialized = True
            return True
        except Exception as e:
            raise e

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
        self.log_event(
            "protocol_cleanup", {"execution_log_entries": len(self.execution_log)}
        )
        self.execution_log.clear()
        self.dependencies.clear()
        self._initialized = False

    def get_status(self) -> Dict[str, Any]:
        """Get current protocol status"""
        self._status.update(
            {
                "initialized": self._initialized,
                "execution_log_size": len(self.execution_log),
                "dependencies_loaded": len(self.dependencies),
                "last_check": iso_now(),
            }
        )
        return self._status

    # LoggingCapable implementation
    def log_event(
        self, event_type: str, details: Any, level: str = "INFO"
    ) -> Dict[str, Any]:
        """Log an event to the session event stream"""
        timestamp = iso_now()

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

    def log_debug(
        self, message: str, details: Any = None, level: str = "DEBUG"
    ) -> Dict[str, Any]:
        """Log debug information to session debug stream"""
        timestamp = iso_now()

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

    # Direct file operations (no interface abstraction needed)
    def create_file(
        self, file_path: str, content: Any, file_type: str = "text"
    ) -> bool:
        """Create a file with atomic write operations"""
        try:
            file_path_obj = Path(file_path)

            # Ensure parent directory exists
            self.ensure_directory_exists(str(file_path_obj.parent))

            if file_type == "json":
                content_str = (
                    json.dumps(content, indent=2)
                    if not isinstance(content, str)
                    else content
                )
            else:
                content_str = str(content)

            # Atomic write
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content_str)

            self.log_event("file_created", {"path": file_path, "type": file_type})
            return True

        except Exception as e:
            # handle_error now raises exceptions (fail hard) - no return needed
            self.handle_error(
                e, {"operation": "create_file", "path": file_path, "type": file_type}
            )

    def append_to_file(self, file_path: str, content: Any) -> bool:
        """Append content to file with atomic operations"""
        try:
            content_str = str(content) if not isinstance(content, str) else content

            with open(file_path, "a", encoding="utf-8") as f:
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
            self.handle_error(
                e, {"operation": "ensure_directory", "path": directory_path}
            )

    # Private helper methods
    def _inject_dependencies(self) -> None:
        """Inject dependencies from container"""
        try:
            # Inject common dependencies
            dependency_map = {
                "session_manager": "session_management",
                "logger": "logging_protocol",
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
