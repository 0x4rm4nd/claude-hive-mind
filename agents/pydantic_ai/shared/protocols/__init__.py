"""
Shared Protocols for Pydantic AI Agents
=======================================
Protocol implementations used across all agents.
"""

from .protocol_interface import (
    ProtocolInterface, 
    LoggingCapable, 
    SessionAware, 
    FileOperationCapable,
    ProtocolMetadata,
    ProtocolRegistry,
    DependencyContainer,
    dependency_container,
    initialize_protocol_system,
    create_protocol_with_dependencies,
    get_protocol_health_status
)
from .session_management import SessionManagement, load_project_env
from .protocol_loader import ProtocolConfig, BaseProtocol
from .worker_management import WorkerManager, WorkerSpec, create_worker_prompts_from_plan, WORKER_CONFIGS
from .config_validator import ConfigurationValidator, ValidationResult, config_validator

__all__ = [
    # Core interfaces
    'ProtocolInterface',
    'LoggingCapable', 
    'SessionAware', 
    'FileOperationCapable',
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
    # Configuration and validation
    'ConfigurationValidator',
    'ValidationResult',
    'config_validator',
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