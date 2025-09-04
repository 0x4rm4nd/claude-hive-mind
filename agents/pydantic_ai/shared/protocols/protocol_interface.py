#!/usr/bin/env python3
"""
Protocol Interface - Common interface for all protocol implementations
=====================================================================
Defines the contract that all protocol implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from datetime import datetime


class ProtocolInterface(ABC):
    """Abstract base class defining the contract for all protocol implementations"""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """
        Initialize the protocol with configuration.

        Args:
            config: Protocol configuration dictionary

        Returns:
            True if initialization successful
        """
        pass

    @abstractmethod
    def validate_config(self, config: Dict[str, Any]) -> bool:
        """
        Validate that configuration contains required fields and values.

        Args:
            config: Configuration dictionary to validate

        Returns:
            True if configuration is valid

        Raises:
            ValueError: If configuration is invalid with specific error message
        """
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """
        Cleanup protocol resources and finalize operations.
        Called when protocol is no longer needed.
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """
        Get current protocol status and health information.

        Returns:
            Dictionary containing status information
        """
        pass

    @abstractmethod
    def handle_error(self, error: Exception, context: Dict[str, Any]) -> bool:
        """
        Handle protocol-specific errors - fail hard implementation.

        Args:
            error: Exception that occurred
            context: Context information about the error

        Returns:
            Should not return - raises the original exception
        """
        pass


class LoggingCapable(ABC):
    """Mixin interface for protocols that support logging"""

    @abstractmethod
    def log_event(
        self, event_type: str, details: Any, level: str = "INFO"
    ) -> Dict[str, Any]:
        """
        Log an event to the session event stream.

        Args:
            event_type: Type of event to log
            details: Event details and data
            level: Log level (INFO, WARNING, ERROR, DEBUG)

        Returns:
            Event dictionary that was logged
        """
        pass

    @abstractmethod
    def log_debug(
        self, message: str, details: Any = None, level: str = "DEBUG"
    ) -> Dict[str, Any]:
        """
        Log debug information to session debug stream.

        Args:
            message: Debug message
            details: Optional additional details
            level: Log level

        Returns:
            Debug entry that was logged
        """
        pass


class SessionAware(ABC):
    """Mixin interface for protocols that work with sessions"""

    @property
    @abstractmethod
    def session_id(self) -> Optional[str]:
        """Get current session identifier"""
        pass

    @property
    @abstractmethod
    def session_path(self) -> Optional[str]:
        """Get current session directory path"""
        pass

    @abstractmethod
    def ensure_session_validity(self) -> bool:
        """
        Ensure session exists and is valid for operations.

        Returns:
            True if session is valid and ready for operations
        """
        pass




class ProtocolMetadata:
    """Metadata container for protocol implementations"""

    def __init__(
        self, name: str, version: str, description: str, capabilities: list = None
    ):
        self.name = name
        self.version = version
        self.description = description
        self.capabilities = capabilities or []
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": self.capabilities,
            "created_at": self.created_at,
        }


class ProtocolRegistry:
    """Registry for managing protocol implementations"""

    _protocols: Dict[str, type] = {}
    _instances: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str, protocol_class: type) -> None:
        """
        Register a protocol implementation.

        Args:
            name: Protocol name identifier
            protocol_class: Protocol implementation class
        """
        if not issubclass(protocol_class, ProtocolInterface):
            raise TypeError(
                f"Protocol class must implement ProtocolInterface: {protocol_class}"
            )

        cls._protocols[name] = protocol_class

    @classmethod
    def get_protocol_class(cls, name: str) -> Optional[type]:
        """Get protocol class by name"""
        return cls._protocols.get(name)

    @classmethod
    def create_instance(
        cls, name: str, config: Dict[str, Any], singleton: bool = False
    ) -> Any:
        """
        Create protocol instance with dependency injection.

        Args:
            name: Protocol name
            config: Configuration for protocol
            singleton: Whether to return singleton instance

        Returns:
            Protocol instance
        """
        if singleton and name in cls._instances:
            return cls._instances[name]

        protocol_class = cls.get_protocol_class(name)
        if not protocol_class:
            raise ValueError(f"Unknown protocol: {name}")

        # Create instance with dependency injection
        instance = protocol_class(config)

        if singleton:
            cls._instances[name] = instance

        return instance

    @classmethod
    def list_available_protocols(cls) -> Dict[str, Dict[str, Any]]:
        """List all available protocols with their metadata"""
        protocols = {}
        for name, protocol_class in cls._protocols.items():
            # Try to get metadata if available
            metadata = getattr(protocol_class, "_metadata", None)
            if metadata and isinstance(metadata, ProtocolMetadata):
                protocols[name] = metadata.to_dict()
            else:
                protocols[name] = {
                    "name": name,
                    "class": protocol_class.__name__,
                    "description": protocol_class.__doc__ or "No description available",
                }
        return protocols


# Dependency injection container
class DependencyContainer:
    """Simple dependency injection container for protocols"""

    def __init__(self):
        self._dependencies: Dict[str, Any] = {}
        self._factories: Dict[str, callable] = {}

    def register_singleton(self, name: str, instance: Any) -> None:
        """Register a singleton dependency"""
        self._dependencies[name] = instance

    def register_factory(self, name: str, factory: callable) -> None:
        """Register a factory function for creating dependencies"""
        self._factories[name] = factory

    def get(self, name: str) -> Any:
        """Get dependency by name"""
        # Check for existing singleton
        if name in self._dependencies:
            return self._dependencies[name]

        # Check for factory
        if name in self._factories:
            instance = self._factories[name]()
            # Store as singleton for future use
            self._dependencies[name] = instance
            return instance

        raise ValueError(f"Unknown dependency: {name}")

    def inject_dependencies(
        self, target: Any, dependency_map: Dict[str, str] = None
    ) -> None:
        """
        Inject dependencies into target object.

        Args:
            target: Object to inject dependencies into
            dependency_map: Mapping of attribute names to dependency names
        """
        if not dependency_map:
            return

        for attr_name, dep_name in dependency_map.items():
            dependency = self.get(dep_name)
            setattr(target, attr_name, dependency)


# Global dependency container instance
dependency_container = DependencyContainer()


# Protocol Setup and Initialization
# =================================
# Merged from protocol_setup.py for consolidated protocol management

def setup_dependencies():
    """Setup dependency injection container with protocol implementations"""

    # Register factory functions for singleton dependencies
    def create_session_management():
        """Factory function for SessionManagement singleton"""
        from .session_management import SessionManagement
        return SessionManagement()

    def create_worker_manager():
        """Factory function for WorkerManager"""
        def worker_manager_factory(session_id):
            from .worker_management import WorkerManager
            return WorkerManager({"session_id": session_id, "agent_name": "worker-manager"})
        return worker_manager_factory

    # Register dependencies in container
    dependency_container.register_factory("session_management", create_session_management)
    dependency_container.register_factory("worker_manager", create_worker_manager)


def register_protocols():
    """Register all protocol implementations with the protocol registry"""
    from .protocol_loader import BaseProtocol
    from .worker_management import WorkerManager

    # Register core protocols
    ProtocolRegistry.register("base_protocol", BaseProtocol)
    ProtocolRegistry.register("worker_manager", WorkerManager)


def initialize_protocol_system():
    """Initialize the complete protocol system with dependencies and registry"""

    # Setup dependency injection
    setup_dependencies()

    # Register protocols
    register_protocols()

    # Test basic functionality
    try:
        # Test that we can create protocol instances
        available_protocols = ProtocolRegistry.list_available_protocols()

        return {
            "status": "success",
            "dependencies_loaded": len(dependency_container._dependencies)
            + len(dependency_container._factories),
            "protocols_registered": len(available_protocols),
            "available_protocols": list(available_protocols.keys()),
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "dependencies_loaded": 0,
            "protocols_registered": 0,
        }


def create_protocol_with_dependencies(
    protocol_name: str, config: Dict[str, Any], inject_deps: bool = True
):
    """
    Create a protocol instance with dependency injection.

    Args:
        protocol_name: Name of protocol to create
        config: Configuration for the protocol
        inject_deps: Whether to inject dependencies automatically

    Returns:
        Protocol instance with dependencies injected
    """

    # Create protocol instance
    protocol_instance = ProtocolRegistry.create_instance(protocol_name, config)

    if inject_deps:
        # Define common dependency mappings
        dependency_mappings = {
            "worker_manager": {"session_manager": "session_management"},
            "base_protocol": {"session_manager": "session_management"},
        }

        # Inject dependencies if mapping exists
        if protocol_name in dependency_mappings:
            dependency_container.inject_dependencies(
                protocol_instance, dependency_mappings[protocol_name]
            )

    return protocol_instance


def get_protocol_health_status() -> Dict[str, Any]:
    """Get health status of all registered protocols"""

    health_status = {
        "overall_status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "protocols": {},
        "dependencies": {},
        "issues": [],
    }

    try:
        # Check dependency container health
        dependency_count = len(dependency_container._dependencies) + len(
            dependency_container._factories
        )
        health_status["dependencies"]["loaded"] = dependency_count
        health_status["dependencies"]["status"] = (
            "healthy" if dependency_count > 0 else "warning"
        )

        # Check registered protocols
        available_protocols = ProtocolRegistry.list_available_protocols()
        health_status["protocols"]["registered"] = len(available_protocols)

        # Test creating instances of each protocol (with minimal config)
        test_config = {"session_id": "health-check", "agent_name": "health-checker"}

        for protocol_name in available_protocols:
            try:
                # Skip protocols that require special setup
                if protocol_name in ["worker_manager"]:
                    health_status["protocols"][protocol_name] = {
                        "status": "skipped",
                        "reason": "requires_special_config",
                    }
                    continue

                instance = ProtocolRegistry.create_instance(protocol_name, test_config)
                if hasattr(instance, "get_status"):
                    protocol_status = instance.get_status()
                    health_status["protocols"][protocol_name] = protocol_status
                else:
                    health_status["protocols"][protocol_name] = {
                        "status": "no_health_check"
                    }

            except Exception as e:
                health_status["protocols"][protocol_name] = {
                    "status": "error",
                    "error": str(e),
                }
                health_status["issues"].append(
                    f"Protocol {protocol_name} failed health check: {str(e)}"
                )

        # Determine overall status
        protocol_errors = [
            p for p in health_status["protocols"].values() if p.get("status") == "error"
        ]
        if protocol_errors:
            health_status["overall_status"] = "degraded"
        elif dependency_count == 0:
            health_status["overall_status"] = "warning"

    except Exception as e:
        health_status["overall_status"] = "failed"
        health_status["issues"].append(f"Health check failed: {str(e)}")

    return health_status
