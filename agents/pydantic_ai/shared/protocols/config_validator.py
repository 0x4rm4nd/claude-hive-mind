#!/usr/bin/env python3
"""
Configuration Validator - Advanced validation for protocol configurations
========================================================================
Provides comprehensive validation with schema definition and error reporting.
"""

from typing import Dict, Any, List, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import re
from datetime import datetime


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
            errors.append(self.error_message or f"Field '{self.field_name}' is required")
            return errors
        
        # Skip further validation if field is empty and not required
        if not self.required and (value is None or value == ""):
            return errors
        
        # Type validation
        if self.validation_type == ValidationType.TYPE_CHECK and self.expected_type:
            if not isinstance(value, self.expected_type):
                errors.append(
                    self.error_message or 
                    f"Field '{self.field_name}' must be of type {self.expected_type.__name__}, got {type(value).__name__}"
                )
        
        # Range validation
        elif self.validation_type == ValidationType.RANGE_CHECK:
            if isinstance(value, (int, float)):
                if self.min_value is not None and value < self.min_value:
                    errors.append(
                        self.error_message or 
                        f"Field '{self.field_name}' must be >= {self.min_value}, got {value}"
                    )
                if self.max_value is not None and value > self.max_value:
                    errors.append(
                        self.error_message or 
                        f"Field '{self.field_name}' must be <= {self.max_value}, got {value}"
                    )
        
        # Pattern validation
        elif self.validation_type == ValidationType.PATTERN_CHECK and self.pattern:
            if isinstance(value, str):
                if not re.match(self.pattern, value):
                    errors.append(
                        self.error_message or 
                        f"Field '{self.field_name}' does not match required pattern: {self.pattern}"
                    )
        
        # Custom validation
        elif self.validation_type == ValidationType.CUSTOM_CHECK and self.custom_validator:
            try:
                is_valid = self.custom_validator(value, config)
                if not is_valid:
                    errors.append(
                        self.error_message or 
                        f"Field '{self.field_name}' failed custom validation"
                    )
            except Exception as e:
                errors.append(f"Custom validation failed for '{self.field_name}': {str(e)}")
        
        # Dependency validation
        elif self.validation_type == ValidationType.DEPENDENCY_CHECK:
            for dependency in self.depends_on:
                if dependency not in config or not config[dependency]:
                    errors.append(
                        self.error_message or 
                        f"Field '{self.field_name}' requires '{dependency}' to be set"
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
    
    def add_required_field(self, field_name: str, expected_type: type, error_message: str = None) -> None:
        """Add a required field validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.TYPE_CHECK,
            required=True,
            expected_type=expected_type,
            error_message=error_message
        )
        self.add_rule(rule)
    
    def add_optional_field(self, field_name: str, expected_type: type, default_value: Any = None) -> None:
        """Add an optional field validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.TYPE_CHECK,
            required=False,
            expected_type=expected_type
        )
        self.add_rule(rule)
    
    def add_range_validation(self, field_name: str, min_value: Union[int, float] = None, 
                           max_value: Union[int, float] = None, error_message: str = None) -> None:
        """Add a range validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.RANGE_CHECK,
            min_value=min_value,
            max_value=max_value,
            error_message=error_message
        )
        self.add_rule(rule)
    
    def add_pattern_validation(self, field_name: str, pattern: str, error_message: str = None) -> None:
        """Add a pattern validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.PATTERN_CHECK,
            pattern=pattern,
            error_message=error_message
        )
        self.add_rule(rule)
    
    def add_custom_validation(self, field_name: str, validator: Callable, error_message: str = None) -> None:
        """Add a custom validation rule"""
        rule = ValidationRule(
            field_name=field_name,
            validation_type=ValidationType.CUSTOM_CHECK,
            custom_validator=validator,
            error_message=error_message
        )
        self.add_rule(rule)
    
    def validate(self, config: Dict[str, Any]) -> 'ValidationResult':
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
                field_results[rule.field_name] = {"status": "error", "errors": field_errors}
            else:
                field_results[rule.field_name] = {"status": "valid", "errors": []}
        
        return ValidationResult(
            is_valid=(len(errors) == 0),
            errors=errors,
            warnings=warnings,
            field_results=field_results,
            schema_name=self.schema_name
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
    
    def get_summary(self) -> Dict[str, Any]:
        """Get validation summary"""
        return {
            "is_valid": self.is_valid,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "schema": self.schema_name,
            "validated_at": self.validated_at
        }
    
    def get_detailed_report(self) -> Dict[str, Any]:
        """Get detailed validation report"""
        return {
            "summary": self.get_summary(),
            "errors": self.errors,
            "warnings": self.warnings,
            "field_results": self.field_results,
            "validation_metadata": {
                "schema_name": self.schema_name,
                "validated_at": self.validated_at
            }
        }


class ConfigurationValidator:
    """Main configuration validator with predefined schemas"""
    
    def __init__(self):
        self.schemas: Dict[str, ConfigurationSchema] = {}
        self._setup_default_schemas()
    
    def _setup_default_schemas(self):
        """Setup default validation schemas for common protocol configurations"""
        
        # Base Protocol Schema
        base_schema = ConfigurationSchema("base_protocol")
        base_schema.add_required_field("session_id", str, "Session ID must be provided as a string")
        base_schema.add_optional_field("agent_name", str)
        base_schema.add_optional_field("timeout", int)
        base_schema.add_optional_field("retries", int)
        base_schema.add_optional_field("prompt_text", str)
        base_schema.add_optional_field("session_path", str)
        
        # Add range validation for timeout and retries
        base_schema.add_range_validation("timeout", min_value=1, max_value=86400, 
                                       error_message="Timeout must be between 1 and 86400 seconds")
        base_schema.add_range_validation("retries", min_value=0, max_value=10,
                                       error_message="Retries must be between 0 and 10")
        
        # Add pattern validation for session_id
        base_schema.add_pattern_validation("session_id", r"^[a-zA-Z0-9\-_]+$",
                                         "Session ID must contain only alphanumeric characters, hyphens, and underscores")
        
        self.schemas["base_protocol"] = base_schema
        
        # Logging Protocol Schema
        logging_schema = ConfigurationSchema("logging_protocol")
        logging_schema.add_required_field("session_id", str)
        logging_schema.add_optional_field("agent_name", str)
        logging_schema.add_optional_field("log_level", str)
        
        # Add custom validation for log_level
        def validate_log_level(value, config):
            valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
            return value in valid_levels
        
        logging_schema.add_custom_validation("log_level", validate_log_level,
                                           "Log level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL")
        
        self.schemas["logging_protocol"] = logging_schema
        
        # Prompt Generator Schema
        prompt_schema = ConfigurationSchema("prompt_generator")
        prompt_schema.add_required_field("session_id", str)
        prompt_schema.add_optional_field("worker_types", list)
        prompt_schema.add_optional_field("complexity_level", int)
        
        prompt_schema.add_range_validation("complexity_level", min_value=1, max_value=10,
                                         error_message="Complexity level must be between 1 and 10")
        
        self.schemas["prompt_generator"] = prompt_schema
    
    def register_schema(self, schema: ConfigurationSchema) -> None:
        """Register a custom validation schema"""
        self.schemas[schema.schema_name] = schema
    
    def validate_config(self, config: Dict[str, Any], schema_name: str = "base_protocol") -> ValidationResult:
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
                schema_name=schema_name
            )
        
        schema = self.schemas[schema_name]
        return schema.validate(config)
    
    def get_available_schemas(self) -> List[str]:
        """Get list of available validation schemas"""
        return list(self.schemas.keys())
    
    def get_schema_info(self, schema_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific schema"""
        if schema_name not in self.schemas:
            return None
        
        schema = self.schemas[schema_name]
        return {
            "name": schema.schema_name,
            "created_at": schema.created_at,
            "rule_count": len(schema.rules),
            "rules": [
                {
                    "field": rule.field_name,
                    "type": rule.validation_type.value,
                    "required": rule.required,
                    "expected_type": rule.expected_type.__name__ if rule.expected_type else None
                }
                for rule in schema.rules
            ]
        }


# Global validator instance
config_validator = ConfigurationValidator()