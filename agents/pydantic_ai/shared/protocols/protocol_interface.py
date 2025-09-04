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
        Handle protocol-specific errors with recovery attempts.

        Args:
            error: Exception that occurred
            context: Context information about the error

        Returns:
            True if error was handled and recovery successful
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


class FileOperationCapable(ABC):
    """Mixin interface for protocols that perform file operations"""

    @abstractmethod
    def create_file(
        self, file_path: str, content: Any, file_type: str = "text"
    ) -> bool:
        """
        Create a file with atomic write operations.

        Args:
            file_path: Path where file should be created
            content: Content to write to file
            file_type: Type of file (text, json, binary)

        Returns:
            True if file created successfully
        """
        pass

    @abstractmethod
    def append_to_file(self, file_path: str, content: Any) -> bool:
        """
        Append content to file with atomic operations.

        Args:
            file_path: Path to file to append to
            content: Content to append

        Returns:
            True if append successful
        """
        pass

    @abstractmethod
    def ensure_directory_exists(self, directory_path: str) -> bool:
        """
        Ensure directory exists, creating if necessary.

        Args:
            directory_path: Path to directory

        Returns:
            True if directory exists or was created successfully
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
