#!/usr/bin/env python3
"""
Architecture Test Suite
======================
Comprehensive tests for the new protocol architecture improvements.
"""

import sys
import traceback
from pathlib import Path

# Add the shared protocols to path
current_dir = Path(__file__).parent
shared_dir = current_dir / "shared"
if str(shared_dir) not in sys.path:
    sys.path.insert(0, str(shared_dir))

def test_interface_system():
    """Test the core interface system"""
    print("🧪 Testing Interface System...")
    
    try:
        from protocols import (
            ProtocolInterface, LoggingCapable, SessionAware, 
            FileOperationCapable, ProtocolRegistry, ProtocolMetadata
        )
        
        # Test that interfaces can be imported
        print("✅ Core interfaces imported successfully")
        
        # Test ProtocolMetadata
        metadata = ProtocolMetadata(
            name="test-protocol",
            version="1.0.0", 
            description="Test protocol",
            capabilities=["logging", "session_aware"]
        )
        metadata_dict = metadata.to_dict()
        assert "name" in metadata_dict
        assert metadata_dict["name"] == "test-protocol"
        print("✅ ProtocolMetadata works correctly")
        
        # Test ProtocolRegistry basic functionality
        available = ProtocolRegistry.list_available_protocols()
        print(f"✅ ProtocolRegistry accessible, found {len(available)} protocols")
        
        return True
        
    except Exception as e:
        print(f"❌ Interface system test failed: {e}")
        traceback.print_exc()
        return False

def test_dependency_injection():
    """Test dependency injection system"""
    print("\n🧪 Testing Dependency Injection...")
    
    try:
        from protocols import DependencyContainer, dependency_container
        
        # Test container creation
        test_container = DependencyContainer()
        print("✅ DependencyContainer created successfully")
        
        # Test singleton registration
        test_container.register_singleton("test_service", "test_value")
        retrieved = test_container.get("test_service")
        assert retrieved == "test_value"
        print("✅ Singleton registration and retrieval works")
        
        # Test factory registration
        def test_factory():
            return {"created": True}
        
        test_container.register_factory("test_factory", test_factory)
        factory_result = test_container.get("test_factory")
        assert factory_result["created"] is True
        print("✅ Factory registration and creation works")
        
        # Test global container exists
        assert dependency_container is not None
        print("✅ Global dependency container available")
        
        return True
        
    except Exception as e:
        print(f"❌ Dependency injection test failed: {e}")
        traceback.print_exc()
        return False

def test_configuration_validation():
    """Test configuration validation system"""
    print("\n🧪 Testing Configuration Validation...")
    
    try:
        from protocols import ConfigurationValidator, config_validator
        
        # Test validator creation
        validator = ConfigurationValidator()
        print("✅ ConfigurationValidator created successfully")
        
        # Test validation with valid config
        valid_config = {
            "session_id": "test-session-123",
            "agent_name": "test-agent",
            "timeout": 300,
            "retries": 2  # Add retries field
        }
        
        result = validator.validate_config(valid_config, "base_protocol")
        if not result.is_valid:
            print(f"❌ Valid config failed: {result.errors}")
            print(f"Config was: {valid_config}")
        assert result.is_valid is True
        print("✅ Valid configuration passes validation")
        
        # Test validation with invalid config  
        invalid_config = {
            "timeout": "invalid_string"  # Should be int
        }
        
        result = validator.validate_config(invalid_config, "base_protocol")
        assert result.is_valid is False
        assert len(result.errors) > 0
        print("✅ Invalid configuration properly rejected")
        
        # Test global validator
        schemas = config_validator.get_available_schemas()
        assert len(schemas) > 0
        print(f"✅ Global validator has {len(schemas)} schemas available")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation test failed: {e}")
        traceback.print_exc()
        return False

def test_error_recovery():
    """Test error recovery system"""
    print("\n🧪 Testing Error Recovery...")
    
    try:
        from protocols import (
            ErrorRecoveryManager, ErrorContext, ErrorSeverity,
            RecoveryStrategy, error_recovery_manager
        )
        
        # Test error recovery manager creation
        recovery_manager = ErrorRecoveryManager()
        print("✅ ErrorRecoveryManager created successfully")
        
        # Test error context creation
        test_error = ValueError("Test error")
        error_context = ErrorContext(
            error=test_error,
            operation="test_operation",
            protocol_name="TestProtocol",
            session_id="test-session",
            severity=ErrorSeverity.MEDIUM
        )
        
        context_dict = error_context.to_dict()
        assert "error_type" in context_dict
        assert "operation" in context_dict
        print("✅ ErrorContext creation and serialization works")
        
        # Test simple recovery function
        def test_operation_success():
            return "success"
            
        def test_operation_fail():
            raise ValueError("Test failure")
        
        # Test successful recovery (no error case)
        recovery_result = recovery_manager.attempt_recovery(
            error_context, test_operation_success
        )
        print("✅ Error recovery system handles successful operations")
        
        # Test global recovery manager
        assert error_recovery_manager is not None
        stats = error_recovery_manager.get_recovery_statistics()
        assert "total_attempts" in stats
        print("✅ Global error recovery manager available with statistics")
        
        return True
        
    except Exception as e:
        print(f"❌ Error recovery test failed: {e}")
        traceback.print_exc()
        return False

def test_protocol_integration():
    """Test BaseProtocol with new architecture"""
    print("\n🧪 Testing Protocol Integration...")
    
    try:
        from protocols import BaseProtocol, ProtocolConfig
        
        # Test protocol creation with valid config
        config = {
            "session_id": "test-session-integration",
            "agent_name": "test-protocol"
        }
        
        protocol = BaseProtocol(config)
        print("✅ BaseProtocol created with new architecture")
        
        # Test interface compliance
        assert hasattr(protocol, 'initialize')
        assert hasattr(protocol, 'validate_config') 
        assert hasattr(protocol, 'cleanup')
        assert hasattr(protocol, 'get_status')
        assert hasattr(protocol, 'handle_error')
        print("✅ BaseProtocol implements ProtocolInterface")
        
        # Test logging capabilities
        assert hasattr(protocol, 'log_event')
        assert hasattr(protocol, 'log_debug')
        print("✅ BaseProtocol implements LoggingCapable")
        
        # Test session awareness
        assert hasattr(protocol, 'session_id')
        assert hasattr(protocol, 'session_path')
        assert hasattr(protocol, 'ensure_session_validity')
        print("✅ BaseProtocol implements SessionAware")
        
        # Test file operations
        assert hasattr(protocol, 'create_file')
        assert hasattr(protocol, 'append_to_file') 
        assert hasattr(protocol, 'ensure_directory_exists')
        print("✅ BaseProtocol implements FileOperationCapable")
        
        # Test status reporting
        status = protocol.get_status()
        assert isinstance(status, dict)
        assert "initialized" in status
        print("✅ Protocol status reporting works")
        
        # Test configuration validation integration
        assert protocol.config.session_id == "test-session-integration"
        assert protocol.config.agent_name == "test-protocol"
        print("✅ Configuration validation integrated")
        
        return True
        
    except Exception as e:
        print(f"❌ Protocol integration test failed: {e}")
        traceback.print_exc()
        return False

def test_system_setup():
    """Test system setup and initialization"""
    print("\n🧪 Testing System Setup...")
    
    try:
        from protocols import initialize_protocol_system, get_protocol_health_status
        
        # Test system initialization
        init_result = initialize_protocol_system()
        assert init_result["status"] == "success"
        assert init_result["dependencies_loaded"] >= 0
        assert init_result["protocols_registered"] >= 0
        print("✅ Protocol system initialization successful")
        print(f"   📊 Dependencies: {init_result['dependencies_loaded']}")
        print(f"   📊 Protocols: {init_result['protocols_registered']}")
        print(f"   📊 Available: {', '.join(init_result['available_protocols'])}")
        
        # Test health monitoring
        health_status = get_protocol_health_status()
        assert "overall_status" in health_status
        assert "protocols" in health_status
        assert "dependencies" in health_status
        print(f"✅ System health check: {health_status['overall_status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ System setup test failed: {e}")
        traceback.print_exc()
        return False

def run_architecture_tests():
    """Run complete architecture test suite"""
    print("🚀 Starting Architecture Test Suite")
    print("=" * 50)
    
    tests = [
        test_interface_system,
        test_dependency_injection,
        test_configuration_validation,
        test_error_recovery,
        test_protocol_integration,
        test_system_setup
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print("🎯 Test Results Summary")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Success Rate: {(passed/(passed+failed)*100):.1f}%")
    
    if failed == 0:
        print("🎉 All architecture tests passed! System is ready.")
        return True
    else:
        print("⚠️  Some tests failed. Review implementation.")
        return False

if __name__ == "__main__":
    success = run_architecture_tests()
    sys.exit(0 if success else 1)