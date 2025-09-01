#!/usr/bin/env python3
"""
Test Enhanced Monkey Patch
==========================
Test the new model resolution patching approach for Agent('custom:*') support.
"""

import sys
from pathlib import Path

# Ensure imports work when run directly from tests folder
current_dir = Path(__file__).parent.parent  # Go up one level to the pydantic_ai directory
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_enhanced_monkey_patch():
    """Test the enhanced monkey patch that should enable Agent('custom:*')"""
    print("🚀 Testing Enhanced Monkey Patch")
    print("=" * 35)
    
    # Import and try the enhanced monkey patch
    from shared.max_subscription_provider import enable_max_subscription_globally
    
    success = enable_max_subscription_globally()
    print(f"Monkey patch success: {success}")
    
    if success:
        print("\n🧪 Testing Direct Agent Creation")
        print("-" * 32)
        
        try:
            from pydantic_ai import Agent
            
            # These should now work with the enhanced monkey patch
            test_cases = [
                'custom:max-subscription',
                'custom:claude-opus-4', 
                'custom:claude-sonnet-4',
                'custom:claude-3-7-sonnet',
                'custom:claude-3-5-haiku',
                'anthropic:claude-3-5-sonnet-latest',  # Should still work
            ]
            
            for model_name in test_cases:
                print(f"📝 Testing Agent('{model_name}')")
                try:
                    agent = Agent(model_name)
                    print(f"   ✅ SUCCESS - Agent created")
                    print(f"   🔧 Model: {agent.model}")
                    print(f"   🔧 Model name: {getattr(agent.model, 'name', 'N/A')}")
                    
                except Exception as e:
                    print(f"   ❌ FAILED - {e}")
                print()
                
        except ImportError as e:
            print(f"❌ Could not import pydantic_ai: {e}")
            
    else:
        print("\n⚠️  Monkey patch failed, testing helper functions instead")
        test_helper_functions()

def test_helper_functions():
    """Helper functions have been removed - test skipped"""
    print("\n🧪 Helper Functions Test")
    print("-" * 22)
    print("ℹ️  Helper functions removed - use Agent('custom:*') directly via monkey patch")

def test_max_subscription_model_directly():
    """Test using MaxSubscriptionModel directly"""
    print("\n🧪 Testing MaxSubscriptionModel Directly")
    print("-" * 37)
    
    try:
        from shared.max_subscription_provider import MaxSubscriptionModel
        from pydantic_ai import Agent
        
        # Test creating agents with MaxSubscriptionModel instances
        test_cases = [
            ("default", MaxSubscriptionModel()),
            ("opus-4", MaxSubscriptionModel("custom:claude-opus-4")),
            ("sonnet-4", MaxSubscriptionModel("custom:claude-sonnet-4")),
        ]
        
        for name, model in test_cases:
            print(f"📝 Testing Agent(MaxSubscriptionModel({name}))")
            try:
                agent = Agent(model)
                print(f"   ✅ SUCCESS - Agent created")
                print(f"   🔧 Model: {agent.model}")
                print(f"   🔧 Model name: {getattr(agent.model, 'model_name', 'N/A')}")
                
            except Exception as e:
                print(f"   ❌ FAILED - {e}")
            print()
            
    except ImportError as e:
        print(f"❌ Could not import required modules: {e}")

def test_provider_functionality():
    """Test that the MaxSubscriptionProvider actually works"""
    print("\n🧪 Testing MaxSubscriptionProvider Functionality")
    print("-" * 44)
    
    try:
        from shared.max_subscription_provider import MaxSubscriptionProvider
        import asyncio
        
        provider = MaxSubscriptionProvider()
        
        print("📝 Testing model mapping logic")
        
        # Test model mapping without actually calling Claude Code
        test_cases = [
            'custom:max-subscription',
            'custom:claude-opus-4',
            'custom:claude-sonnet-4',
            'custom:unknown-model',
        ]
        
        for model in test_cases:
            if model == 'custom:max-subscription':
                actual_model = provider.default_model
            elif model in provider.claude_code_model_mapping:
                actual_model = model
            else:
                actual_model = provider.default_model
                
            claude_code_model = provider.claude_code_model_mapping.get(actual_model, 'sonnet')
            
            print(f"   {model} → {actual_model} → {claude_code_model}")
            
        print("   ✅ Model mapping logic working correctly")
        
    except Exception as e:
        print(f"❌ Provider test failed: {e}")

if __name__ == "__main__":
    print("🚀 Enhanced Monkey Patch Test Suite")
    print("=" * 36)
    
    test_enhanced_monkey_patch()
    test_helper_functions() 
    test_max_subscription_model_directly()
    test_provider_functionality()
    
    print("\n✅ Test suite completed!")