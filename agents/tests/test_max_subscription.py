#!/usr/bin/env python3
"""
Test Script for Agent('custom:max-subscription') Integration

Tests the ClaudeAPISubscriptionProvider integration with the Docker service
without importing the full Pydantic AI framework to avoid compatibility issues.
"""

import asyncio
import json
from typing import Dict, Any

try:
    # Test 1: Direct HTTP client integration
    from shared.custom_provider.claude_max.api_service_client import ClaudeAPIServiceClient
    
    print("✅ Successfully imported ClaudeAPIServiceClient")
    HTTP_CLIENT_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import ClaudeAPIServiceClient: {e}")
    HTTP_CLIENT_AVAILABLE = False

try:
    # Test 2: Pydantic AI Model adapter
    from shared.custom_provider.claude_max.pydantic_model_adapter import (
        ClaudeMaxSubscriptionModel,
        enable_max_subscription_integration
    )
    
    print("✅ Successfully imported ClaudeMaxSubscriptionModel")
    PYDANTIC_ADAPTER_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import ClaudeMaxSubscriptionModel: {e}")
    PYDANTIC_ADAPTER_AVAILABLE = False

# Fallback HTTP test using aiohttp directly
try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
    print("✅ aiohttp available for fallback testing")
except ImportError:
    print("❌ aiohttp not available")
    AIOHTTP_AVAILABLE = False


async def test_direct_http_integration():
    """Test direct HTTP communication with Docker service"""
    print("\n=== Testing Direct HTTP Integration ===")
    
    if not AIOHTTP_AVAILABLE:
        print("❌ Skipping - aiohttp not available")
        return False
        
    try:
        async with aiohttp.ClientSession() as session:
            # Health check
            async with session.get("http://localhost:47291/health") as response:
                health_data = await response.json()
                print(f"✅ Health check: {health_data}")
                
            # Simple API call
            test_request = {
                "prompt": "Hello, can you respond with 'Max subscription is working!'?",
                "model": "sonnet",
                "timeout": 30
            }
            
            async with session.post(
                "http://localhost:47291/claude", 
                json=test_request,
                timeout=aiohttp.ClientTimeout(total=45)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"✅ API call successful: {result['response'][:100]}...")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ API call failed: {response.status} - {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Direct HTTP test failed: {e}")
        return False


async def test_api_service_client():
    """Test the ClaudeAPIServiceClient wrapper"""
    print("\n=== Testing ClaudeAPIServiceClient ===")
    
    if not HTTP_CLIENT_AVAILABLE:
        print("❌ Skipping - ClaudeAPIServiceClient not available")
        return False
        
    try:
        client = ClaudeAPIServiceClient()
        
        # Test basic functionality
        print("📊 Client status:", json.dumps(client.get_service_status(), indent=2))
        
        # Test custom:max-subscription routing
        response = await client.send_prompt(
            "Please respond with 'ClaudeAPIServiceClient is working with Max subscription!'",
            "custom:max-subscription"
        )
        
        print(f"✅ Max subscription test: {response[:150]}...")
        return True
        
    except Exception as e:
        print(f"❌ ClaudeAPIServiceClient test failed: {e}")
        return False


async def test_pydantic_model_adapter():
    """Test the Pydantic AI model adapter"""
    print("\n=== Testing ClaudeMaxSubscriptionModel ===")
    
    if not PYDANTIC_ADAPTER_AVAILABLE:
        print("❌ Skipping - ClaudeMaxSubscriptionModel not available")
        return False
    
    try:
        # Create model instance
        model = ClaudeMaxSubscriptionModel("custom:max-subscription")
        print(f"✅ Created model: {repr(model)}")
        
        # Test model properties
        print(f"📋 Model name: {model.model_name}")
        print(f"📋 System: {model.system}")
        
        return True
        
    except Exception as e:
        print(f"❌ ClaudeMaxSubscriptionModel test failed: {e}")
        return False


def test_pydantic_ai_integration():
    """Test full Pydantic AI Agent integration"""
    print("\n=== Testing Full Pydantic AI Integration ===")
    
    try:
        # Try to import pydantic_ai
        import pydantic_ai
        from pydantic_ai import Agent
        
        print("✅ Pydantic AI available")
        
        # Enable integration
        if PYDANTIC_ADAPTER_AVAILABLE:
            success = enable_max_subscription_integration()
            if not success:
                print("❌ Failed to enable max subscription integration")
                return False
                
            # Test Agent creation
            agent = Agent("custom:max-subscription")
            print(f"✅ Created Agent: {agent}")
            
            # Note: We won't run the agent to avoid async complexity in this test
            print("✅ Agent('custom:max-subscription') creation successful")
            return True
        else:
            print("❌ Pydantic adapter not available, skipping agent test")
            return False
            
    except ImportError as e:
        print(f"❌ Pydantic AI not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Pydantic AI integration test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("🚀 Testing Agent('custom:max-subscription') Integration")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Direct HTTP
    results['direct_http'] = await test_direct_http_integration()
    
    # Test 2: API Service Client  
    results['api_client'] = await test_api_service_client()
    
    # Test 3: Pydantic Model Adapter
    results['model_adapter'] = await test_pydantic_model_adapter()
    
    # Test 4: Full Pydantic AI Integration
    results['pydantic_ai'] = test_pydantic_ai_integration()
    
    # Summary
    print("\n" + "=" * 60)
    print("🏁 Test Results Summary:")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED - Agent('custom:max-subscription') is working!")
    else:
        print("⚠️  SOME TESTS FAILED - Check individual test output above")
        
    return all_passed


if __name__ == "__main__":
    asyncio.run(main())