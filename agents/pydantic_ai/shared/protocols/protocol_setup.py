#!/usr/bin/env python3
"""
Protocol Setup - Dependency injection and protocol registration
===============================================================
Sets up dependency injection container and registers all protocols.
"""

from typing import Dict, Any
from .protocol_interface import ProtocolRegistry, dependency_container
from .session_management import SessionManagement
from .protocol_loader import BaseProtocol
from .prompt_generator import PromptGenerator


def setup_dependencies():
    """Setup dependency injection container with protocol implementations"""
    
    # Register factory functions for singleton dependencies
    def create_session_management():
        """Factory function for SessionManagement singleton"""
        return SessionManagement()
    
    
    def create_prompt_generator():
        """Factory function for PromptGenerator"""
        def prompt_generator_factory(session_id):
            return PromptGenerator(session_id)
        return prompt_generator_factory
    
    # Register dependencies in container
    dependency_container.register_factory("session_management", create_session_management)
    dependency_container.register_factory("prompt_generator", create_prompt_generator)


def register_protocols():
    """Register all protocol implementations with the protocol registry"""
    
    # Register core protocols
    ProtocolRegistry.register("base_protocol", BaseProtocol)
    ProtocolRegistry.register("prompt_generator", PromptGenerator)
    
    # Could register more specialized protocols here
    # ProtocolRegistry.register("worker_prompt_protocol", WorkerPromptProtocol)


def initialize_protocol_system():
    """Initialize the complete protocol system with dependencies and registry"""
    
    # Setup dependency injection
    setup_dependencies()
    
    # Register protocols
    register_protocols()
    
    # Test basic functionality
    try:
        # Test session management dependency
        session_manager = dependency_container.get("session_management")
        
        # Test that we can create protocol instances
        available_protocols = ProtocolRegistry.list_available_protocols()
        
        return {
            "status": "success",
            "dependencies_loaded": len(dependency_container._dependencies) + len(dependency_container._factories),
            "protocols_registered": len(available_protocols),
            "available_protocols": list(available_protocols.keys())
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "dependencies_loaded": 0,
            "protocols_registered": 0
        }


def create_protocol_with_dependencies(protocol_name: str, config: Dict[str, Any], inject_deps: bool = True):
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
            "prompt_generator": {
                "session_manager": "session_management"
            },
            "base_protocol": {
                "session_manager": "session_management"
            }
        }
        
        # Inject dependencies if mapping exists
        if protocol_name in dependency_mappings:
            dependency_container.inject_dependencies(
                protocol_instance, 
                dependency_mappings[protocol_name]
            )
    
    return protocol_instance


def get_protocol_health_status() -> Dict[str, Any]:
    """Get health status of all registered protocols"""
    
    health_status = {
        "overall_status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "protocols": {},
        "dependencies": {},
        "issues": []
    }
    
    try:
        # Check dependency container health
        dependency_count = len(dependency_container._dependencies) + len(dependency_container._factories)
        health_status["dependencies"]["loaded"] = dependency_count
        health_status["dependencies"]["status"] = "healthy" if dependency_count > 0 else "warning"
        
        # Check registered protocols
        available_protocols = ProtocolRegistry.list_available_protocols()
        health_status["protocols"]["registered"] = len(available_protocols)
        
        # Test creating instances of each protocol (with minimal config)
        test_config = {"session_id": "health-check", "agent_name": "health-checker"}
        
        for protocol_name in available_protocols:
            try:
                # Skip protocols that require special setup
                if protocol_name in ["prompt_generator"]:
                    health_status["protocols"][protocol_name] = {"status": "skipped", "reason": "requires_special_config"}
                    continue
                    
                instance = ProtocolRegistry.create_instance(protocol_name, test_config)
                if hasattr(instance, 'get_status'):
                    protocol_status = instance.get_status()
                    health_status["protocols"][protocol_name] = protocol_status
                else:
                    health_status["protocols"][protocol_name] = {"status": "no_health_check"}
                    
            except Exception as e:
                health_status["protocols"][protocol_name] = {"status": "error", "error": str(e)}
                health_status["issues"].append(f"Protocol {protocol_name} failed health check: {str(e)}")
        
        # Determine overall status
        protocol_errors = [p for p in health_status["protocols"].values() if p.get("status") == "error"]
        if protocol_errors:
            health_status["overall_status"] = "degraded"
        elif dependency_count == 0:
            health_status["overall_status"] = "warning"
            
    except Exception as e:
        health_status["overall_status"] = "failed"
        health_status["issues"].append(f"Health check failed: {str(e)}")
    
    return health_status


# Import required for health status function
from datetime import datetime
from .protocol_loader import BaseProtocol