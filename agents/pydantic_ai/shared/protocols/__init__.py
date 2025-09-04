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
    dependency_container
)
from .session_management import SessionManagement
# LoggingProtocol deprecated - use LoggingCapable mixin from BaseProtocol
from .protocol_loader import ProtocolConfig, BaseProtocol
from .worker_prompt_protocol import WorkerPromptProtocol
from .env_loader import load_project_env
from .prompt_generator import PromptGenerator, create_worker_prompts_from_plan
from .config_validator import ConfigurationValidator, ValidationResult, config_validator
from .protocol_setup import initialize_protocol_system, create_protocol_with_dependencies, get_protocol_health_status

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
    'ProtocolConfig', 
    'BaseProtocol',
    'WorkerPromptProtocol',
    'load_project_env',
    'PromptGenerator',
    'create_worker_prompts_from_plan',
    # Architectural improvements
    'ConfigurationValidator',
    'ValidationResult',
    'config_validator',
    'initialize_protocol_system',
    'create_protocol_with_dependencies',
    'get_protocol_health_status',
    'PROTOCOL_SYSTEM_STATUS'
]

# Initialize the protocol system when package is imported
_initialization_result = initialize_protocol_system()

# Store initialization status for debugging if needed
PROTOCOL_SYSTEM_STATUS = _initialization_result