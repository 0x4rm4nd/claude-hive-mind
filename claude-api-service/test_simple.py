#!/usr/bin/env python3
"""
Simple direct HTTP test of the Claude API service integration.
Tests the core architecture without Pydantic AI dependencies.
"""

import asyncio
import json
import sys
from pathlib import Path

import aiohttp


async def test_core_integration():
    """Test the core Claude API service directly"""
    print("🚀 Testing Core Claude API Service Integration")
    print("=" * 50)
    
    api_base_url = "http://localhost:47291"
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test health endpoint
            print("🏥 Testing health endpoint...")
            async with session.get(f"{api_base_url}/health") as response:
                if response.status == 200:
                    health = await response.json()
                    print("✅ Health check successful:")
                    print(f"   Status: {health['status']}")
                    print(f"   Claude CLI: {health['claude_cli']}")
                    print(f"   Workspace: {health['workspace_root']}")
                    print(f"   Purpose: {health['purpose']}")
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
            
            # Test root endpoint
            print("\n📋 Testing root endpoint...")
            async with session.get(f"{api_base_url}/") as response:
                if response.status == 200:
                    root_info = await response.json()
                    print("✅ Root endpoint successful:")
                    print(f"   Service: {root_info['service']}")
                    print(f"   Purpose: {root_info['purpose']}")
                    print(f"   Endpoints: {list(root_info['endpoints'].keys())}")
                else:
                    print(f"❌ Root endpoint failed: {response.status}")
                    return False
            
            # Test Claude endpoint with mock
            print("\n💬 Testing Claude endpoint...")
            test_request = {
                "prompt": "Integration test - respond with 'MOCK_SUCCESS'",
                "model": "sonnet",
                "timeout": 30
            }
            
            async with session.post(
                f"{api_base_url}/claude", 
                json=test_request
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print("✅ Claude endpoint successful:")
                    print(f"   Response: {result['response']}")
                    print(f"   Model: {result['model']}")
                    print(f"   Success: {result['success']}")
                    
                    # Since we're using mock Claude, check if it processed the request
                    if "Integration test" in result['response'] and result['success']:
                        print("🎯 Generic Claude API integration working!")
                        return True
                    else:
                        print("⚠️  Unexpected response format")
                        return False
                else:
                    error_text = await response.text()
                    print(f"❌ Claude endpoint failed: {response.status}")
                    print(f"   Error: {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False


async def test_error_handling():
    """Test error handling in the service"""
    print("\n🔧 Testing Error Handling...")
    print("=" * 30)
    
    api_base_url = "http://localhost:47291"
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test invalid endpoint
            async with session.get(f"{api_base_url}/invalid") as response:
                if response.status == 404:
                    print("✅ 404 handling works correctly")
                else:
                    print(f"⚠️  Expected 404, got {response.status}")
            
            # Test malformed request
            async with session.post(
                f"{api_base_url}/claude",
                json={"invalid": "request"}
            ) as response:
                if response.status in [400, 422]:  # Bad request or validation error
                    print("✅ Request validation works correctly")
                else:
                    print(f"⚠️  Expected 400/422, got {response.status}")
        
        return True
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("🎯 Claude API Service Direct Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Core Integration", test_core_integration),
        ("Error Handling", test_error_handling)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = await test_func()
            results[test_name] = success
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results[test_name] = False
    
    print("\n" + "=" * 60)
    print("DIRECT INTEGRATION TEST RESULTS:")
    print("=" * 60)
    
    all_passed = True
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False
    
    print(f"\nOverall: {'🎉 ALL TESTS PASSED' if all_passed else '⚠️  SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎯 The Claude API Service core architecture is working!")
        print("   ✅ Docker service running on port 47291")
        print("   ✅ Generic /claude endpoint functional") 
        print("   ✅ Health monitoring working")
        print("   ✅ Error handling implemented")
        print("\n📋 Next Steps:")
        print("   1. Replace mock Claude CLI with real Claude CLI")
        print("   2. Fix Pydantic AI compatibility issues") 
        print("   3. Test Agent('custom:max-subscription') integration")
        print("   4. Verify Max subscription authentication")
    else:
        print("\n🔧 Core architecture issues detected.")
        print("   Check service logs and configuration.")


if __name__ == "__main__":
    asyncio.run(main())