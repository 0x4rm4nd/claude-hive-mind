#!/usr/bin/env python3
"""
Test Max Subscription Provider
=============================
Simple test to validate the model mapping and provider functionality.
"""

import sys
from pathlib import Path

# Ensure imports work when run directly from tests folder
current_dir = Path(__file__).parent.parent  # Go up one level to the pydantic_ai directory
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

def test_model_mapping():
    """Test the model mapping functionality"""
    from shared.max_subscription_provider import MaxSubscriptionProvider
    
    provider = MaxSubscriptionProvider()
    
    print("🧪 Testing Max Subscription Provider Model Mapping")
    print("=" * 50)
    
    # Test cases
    test_cases = [
        ('custom:max-subscription', 'custom:claude-sonnet-4', 'sonnet'),
        ('custom:claude-opus-4', 'custom:claude-opus-4', 'opus'), 
        ('custom:claude-sonnet-4', 'custom:claude-sonnet-4', 'sonnet'),
        ('custom:claude-3-7-sonnet', 'custom:claude-3-7-sonnet', 'claude-3-7-sonnet-20250219'),
        ('custom:claude-3-5-haiku', 'custom:claude-3-5-haiku', 'haiku'),
        ('unknown-model', 'custom:claude-sonnet-4', 'sonnet'),  # Should fallback to default
    ]
    
    for input_model, expected_actual, expected_claude_code in test_cases:
        print(f"\n📝 Testing: {input_model}")
        
        # Simulate the model selection logic
        if input_model == 'custom:max-subscription':
            actual_model = provider.default_model
        elif input_model.startswith('custom:claude-'):
            actual_model = input_model
        else:
            actual_model = provider.default_model
        
        claude_code_model = provider.claude_code_model_mapping.get(actual_model, 'sonnet')
        
        print(f"   → Actual model: {actual_model}")
        print(f"   → Claude Code param: {claude_code_model}")
        
        # Validate results
        if actual_model == expected_actual and claude_code_model == expected_claude_code:
            print("   ✅ PASS")
        else:
            print(f"   ❌ FAIL - Expected actual: {expected_actual}, claude_code: {expected_claude_code}")
    
    print(f"\n🔧 Default model: {provider.default_model}")
    print(f"🔄 Fallback model: {provider.fallback_model}")

def test_message_formatting():
    """Test message formatting for Claude Code"""
    from shared.max_subscription_provider import MaxSubscriptionProvider
    
    provider = MaxSubscriptionProvider()
    
    print("\n🧪 Testing Message Formatting")
    print("=" * 30)
    
    # Test simple messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thanks!"}
    ]
    
    formatted = provider._format_messages_for_claude_code(messages)
    print("📝 Formatted messages:")
    print(formatted)
    
    # Test multi-part content (should extract text only)
    complex_messages = [
        {
            "role": "user", 
            "content": [
                {"type": "text", "text": "Analyze this image"},
                {"type": "image", "source": "data:image/..."},
                {"type": "text", "text": "and tell me what you see"}
            ]
        }
    ]
    
    formatted_complex = provider._format_messages_for_claude_code(complex_messages)
    print(f"\n📝 Complex message formatted:")
    print(formatted_complex)

def test_direct_agent_creation():
    """Test that the monkey patch enables custom: models globally"""
    print("\n🧪 Testing Direct Agent Creation")
    print("=" * 33)
    
    try:
        from pydantic_ai import Agent
        
        # Test creating agents with custom models via direct string usage
        test_models = [
            'custom:max-subscription',
            'custom:claude-opus-4', 
            'custom:claude-sonnet-4',
            'custom:claude-3-7-sonnet',
            'custom:claude-3-5-haiku',
            'anthropic:claude-3-5-sonnet-latest'  # Should use original behavior
        ]
        
        for model in test_models:
            print(f"📝 Testing Agent('{model}')")
            try:
                agent = Agent(model)
                print(f"   ✅ Agent created successfully")
                print(f"   🔧 Model: {getattr(agent.model, 'model_name', getattr(agent.model, 'name', str(agent.model)))}")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")
            print()
                
    except ImportError as e:
        print(f"❌ Could not import pydantic_ai: {e}")
        print("ℹ️  This is expected if pydantic_ai is not installed")

if __name__ == "__main__":
    print("🚀 Max Subscription Provider Test Suite")
    print("=" * 40)
    
    test_model_mapping()
    test_message_formatting()
    test_direct_agent_creation()
    
    print("\n✅ Test suite completed!")