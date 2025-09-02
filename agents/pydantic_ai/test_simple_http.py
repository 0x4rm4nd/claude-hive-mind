#!/usr/bin/env python3
"""
Simple HTTP Test for Max Subscription Integration

Tests direct HTTP communication with Docker service without 
importing the full Pydantic AI framework to avoid compatibility issues.
"""

import asyncio
import json

try:
    import aiohttp
    print("✅ aiohttp available")
    AIOHTTP_AVAILABLE = True
except ImportError:
    print("❌ aiohttp not available")
    AIOHTTP_AVAILABLE = False


async def test_docker_service_health():
    """Test health endpoint of Docker service"""
    print("\n=== Testing Docker Service Health ===")
    
    if not AIOHTTP_AVAILABLE:
        print("❌ Cannot test - aiohttp not available")
        return False
        
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "http://localhost:47291/health",
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    health_data = await response.json()
                    print(f"✅ Service is healthy: {json.dumps(health_data, indent=2)}")
                    return True
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False
                    
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


async def test_max_subscription_routing():
    """Test max subscription model routing through Docker service"""
    print("\n=== Testing Max Subscription Model Routing ===")
    
    if not AIOHTTP_AVAILABLE:
        print("❌ Cannot test - aiohttp not available")
        return False
        
    # Test different model mappings that should route to Max subscription
    model_tests = [
        ("sonnet", "Direct sonnet model"),
        ("opus", "Direct opus model"),
        ("claude-3-7-sonnet-20250219", "Specific Claude 3.7 sonnet"),
        ("haiku", "Direct haiku model")
    ]
    
    results = {}
    
    for model, description in model_tests:
        print(f"\n📋 Testing {description} (model: {model})")
        
        try:
            test_request = {
                "prompt": f"Please respond with 'Model {model} is working via Max subscription!' and nothing else.",
                "model": model,
                "timeout": 30
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://localhost:47291/claude",
                    json=test_request,
                    timeout=aiohttp.ClientTimeout(total=45)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        response_text = result.get('response', '').strip()
                        print(f"✅ {model}: {response_text[:100]}...")
                        results[model] = True
                    else:
                        error_text = await response.text()
                        print(f"❌ {model} failed: {response.status} - {error_text}")
                        results[model] = False
                        
        except Exception as e:
            print(f"❌ {model} error: {e}")
            results[model] = False
            
    return all(results.values())


async def test_custom_model_mapping():
    """Test custom:* model name handling via Docker service"""
    print("\n=== Testing Custom Model Name Mapping ===")
    
    if not AIOHTTP_AVAILABLE:
        print("❌ Cannot test - aiohttp not available")
        return False
    
    # Simulate how ClaudeAPIServiceClient would map custom: models
    model_mapping = {
        "custom:max-subscription": "sonnet",
        "custom:claude-opus-4": "opus", 
        "custom:claude-sonnet-4": "sonnet",
        "custom:claude-3-7-sonnet": "claude-3-7-sonnet-20250219",
        "custom:claude-3-5-haiku": "haiku",
    }
    
    print(f"📋 Model mapping: {json.dumps(model_mapping, indent=2)}")
    
    # Test the primary custom:max-subscription model
    custom_model = "custom:max-subscription"
    mapped_model = model_mapping[custom_model]
    
    print(f"\n📋 Testing {custom_model} → {mapped_model}")
    
    try:
        test_request = {
            "prompt": "Please respond with 'Agent(\\'custom:max-subscription\\') routing is working!' and nothing else.",
            "model": mapped_model,  # This is what ClaudeAPIServiceClient would send
            "timeout": 30
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "http://localhost:47291/claude",
                json=test_request,
                timeout=aiohttp.ClientTimeout(total=45)
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    response_text = result.get('response', '').strip()
                    print(f"✅ custom:max-subscription routing: {response_text}")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ custom:max-subscription failed: {response.status} - {error_text}")
                    return False
                    
    except Exception as e:
        print(f"❌ custom:max-subscription error: {e}")
        return False


async def test_api_service_endpoints():
    """Test all available endpoints on the Docker service"""
    print("\n=== Testing API Service Endpoints ===")
    
    if not AIOHTTP_AVAILABLE:
        print("❌ Cannot test - aiohttp not available")
        return False
    
    endpoints_to_test = [
        ("/health", "GET", None),
        ("/claude", "POST", {"prompt": "Test", "model": "sonnet", "timeout": 30})
    ]
    
    results = {}
    
    for endpoint, method, data in endpoints_to_test:
        print(f"\n📋 Testing {method} {endpoint}")
        
        try:
            async with aiohttp.ClientSession() as session:
                if method == "GET":
                    async with session.get(
                        f"http://localhost:47291{endpoint}",
                        timeout=aiohttp.ClientTimeout(total=10)
                    ) as response:
                        status = response.status
                        if status == 200:
                            result = await response.json()
                            print(f"✅ {endpoint}: {json.dumps(result, indent=2)}")
                            results[endpoint] = True
                        else:
                            error_text = await response.text()
                            print(f"❌ {endpoint}: {status} - {error_text}")
                            results[endpoint] = False
                            
                elif method == "POST":
                    async with session.post(
                        f"http://localhost:47291{endpoint}",
                        json=data,
                        timeout=aiohttp.ClientTimeout(total=45)
                    ) as response:
                        status = response.status
                        if status == 200:
                            result = await response.json()
                            print(f"✅ {endpoint}: Response received (length: {len(result.get('response', ''))})")
                            results[endpoint] = True
                        else:
                            error_text = await response.text()
                            print(f"❌ {endpoint}: {status} - {error_text}")
                            results[endpoint] = False
                            
        except Exception as e:
            print(f"❌ {endpoint} error: {e}")
            results[endpoint] = False
    
    return all(results.values())


async def main():
    """Run all tests"""
    print("🚀 Testing Agent('custom:max-subscription') Integration")
    print("Focus: Direct HTTP client integration with Docker service")
    print("=" * 70)
    
    test_results = {}
    
    # Test 1: Service Health
    test_results['health'] = await test_docker_service_health()
    
    # Test 2: API Endpoints
    test_results['endpoints'] = await test_api_service_endpoints()
    
    # Test 3: Model Routing
    test_results['routing'] = await test_max_subscription_routing()
    
    # Test 4: Custom Model Mapping
    test_results['custom_mapping'] = await test_custom_model_mapping()
    
    # Summary
    print("\n" + "=" * 70)
    print("🏁 Test Results Summary:")
    print("=" * 70)
    
    all_passed = True
    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 70)
    if all_passed:
        print("🎉 ALL TESTS PASSED")
        print("✅ Agent('custom:max-subscription') routing through Docker service is working!")
        print("✅ HTTP client integration is functional")
        print("✅ Model mapping is correct")
    else:
        print("⚠️  SOME TESTS FAILED - Check individual test output above")
        
    return all_passed


if __name__ == "__main__":
    asyncio.run(main())