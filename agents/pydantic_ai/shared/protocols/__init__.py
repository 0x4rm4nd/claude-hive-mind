"""
Shared Protocols for Pydantic AI Agents
=======================================
Protocol implementations used across all agents.
"""

from .protocol_interface import (
    ProtocolInterface, 
    LoggingCapable, 
    SessionAware, 
    ProtocolMetadata,
    ProtocolRegistry,
    DependencyContainer,
    dependency_container,
    initialize_protocol_system,
    create_protocol_with_dependencies,
    get_protocol_health_status
)
from .session_management import SessionManagement, load_project_env
from .protocol_loader import (
    ProtocolConfig, 
    BaseProtocol,
    ConfigurationValidator, 
    ValidationResult, 
    config_validator,
    ValidationType,
    ValidationRule,
    ConfigurationSchema
)
from .worker_management import WorkerManager, WorkerSpec, create_worker_prompts_from_plan, WORKER_CONFIGS

__all__ = [
    # Core interfaces
    'ProtocolInterface',
    'LoggingCapable', 
    'SessionAware', 
    'ProtocolMetadata',
    'ProtocolRegistry',
    'DependencyContainer',
    'dependency_container',
    # Protocol implementations
    'SessionManagement',
    'load_project_env',
    'ProtocolConfig', 
    'BaseProtocol',
    'WorkerManager',
    'WorkerSpec',
    'create_worker_prompts_from_plan',
    'WORKER_CONFIGS',
    # Configuration and validation (integrated from config_validator)
    'ConfigurationValidator',
    'ValidationResult',
    'config_validator',
    'ValidationType',
    'ValidationRule',
    'ConfigurationSchema',
    # System initialization
    'initialize_protocol_system',
    'create_protocol_with_dependencies',
    'get_protocol_health_status',
    'PROTOCOL_SYSTEM_STATUS'
]

# Initialize the protocol system when package is imported
_initialization_result = initialize_protocol_system()

# Store initialization status for debugging if needed
PROTOCOL_SYSTEM_STATUS = _initialization_result