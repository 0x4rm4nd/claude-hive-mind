#!/usr/bin/env python3
"""
Test script for Claude API Service integration.

Tests the complete workflow from Pydantic AI to Claude API service.
"""

import asyncio
import sys
import json
from pathlib import Path

# Add the parent directory to Python path for imports
sys.path.append(str(Path(__file__).parent.parent / "agents" / "pydantic_ai"))

from shared.claude_integration import ClaudeAPISubscriptionProvider
from pydantic_ai import Agent


async def test_provider_integration():
    """Test the ClaudeAPISubscriptionProvider integration"""
    print("=== Claude API Service Integration Test ===\n")

    provider = ClaudeAPISubscriptionProvider()

    print("📊 Provider Status:")
    status = provider.get_service_status()
    print(json.dumps(status, indent=2))

    print("\n🔧 Testing service health...")
    healthy = await provider._check_service_health()
    print(f"Service healthy: {healthy}")

    if not healthy:
        print("❌ Service not healthy - start manually with:")
        print("cd .claude/claude-api-service && docker-compose up -d")
        return False

    print("\n🧠 Testing complexity assessment...")
    try:
        complexity = await provider.call_complexity_assessment(
            "Implement user authentication with JWT tokens and rate limiting"
        )
        print("✅ Complexity assessment successful:")
        print(json.dumps(complexity, indent=2))
    except Exception as e:
        print(f"❌ Complexity assessment failed: {e}")
        return False

    print("\n💬 Testing direct chat...")
    try:
        # Create a mock message for testing
        mock_messages = [
            type(
                "MockMessage",
                (),
                {
                    "content": "Test message for API service integration - respond with SUCCESS",
                    "role": "user",
                },
            )()
        ]

        response = await provider.request_structured_response(
            mock_messages, "custom:max-subscription"
        )
        print("✅ Direct chat successful:")
        print(f"Response: {response}")

        if "SUCCESS" in response:
            print("🎯 Integration working correctly!")
            return True
        else:
            print("⚠️  Unexpected response content")
            return False

    except Exception as e:
        print(f"❌ Direct chat failed: {e}")
        return False


async def test_pydantic_agent_integration():
    """Test Pydantic AI Agent integration with custom models"""
    print("\n=== Pydantic AI Agent Integration Test ===\n")

    try:
        print("🤖 Testing Agent creation with custom:max-subscription...")
        agent = Agent(
            "custom:max-subscription",
            system_prompt="You are a test assistant. Respond with 'PYDANTIC_INTEGRATION_SUCCESS' followed by a brief confirmation.",
        )

        print("🧠 Testing agent execution...")
        result = await agent.run_async(
            "Test the Pydantic AI integration with Claude API service"
        )

        print("✅ Pydantic AI Agent integration successful:")
        print(f"Response: {result.data}")

        if "PYDANTIC_INTEGRATION_SUCCESS" in str(result.data):
            print("🎯 Full integration chain working correctly!")
            return True
        else:
            print("⚠️  Unexpected response format")
            return False

    except Exception as e:
        print(f"❌ Pydantic AI Agent integration failed: {e}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")
        return False


async def test_scribe_integration():
    """Test scribe runner integration"""
    print("\n=== Scribe Integration Test ===\n")

    try:
        # Import scribe worker
        from scribe.runner import ScribeWorker

        worker = ScribeWorker()

        print("🔍 Testing scribe session creation...")
        result = worker.run(
            "",  # Empty session_id triggers create mode
            "Test scribe integration with Claude API service",
            "custom:max-subscription",
        )

        print("✅ Scribe session creation successful:")
        print(f"Session ID: {result.session_id}")
        print(f"Complexity: {result.complexity_level}")
        print(f"Path: {result.session_path}")

        return True

    except Exception as e:
        print(f"❌ Scribe integration failed: {e}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")
        return False


async def test_api_service_endpoints():
    """Test Claude API service endpoints directly"""
    print("\n=== API Service Endpoints Test ===\n")

    import aiohttp

    base_url = "http://localhost:47291"

    try:
        async with aiohttp.ClientSession() as session:
            # Test health endpoint
            print("🏥 Testing health endpoint...")
            async with session.get(f"{base_url}/health") as response:
                if response.status == 200:
                    health = await response.json()
                    print("✅ Health check successful:")
                    print(json.dumps(health, indent=2))
                else:
                    print(f"❌ Health check failed: {response.status}")
                    return False

            # Test root endpoint  
            print("\n📋 Testing root endpoint...")
            async with session.get(f"{base_url}/") as response:
                if response.status == 200:
                    root_info = await response.json()
                    print("✅ Root endpoint successful:")
                    print(f"Service: {root_info['service']}")
                    print(f"Purpose: {root_info['purpose']}")
                else:
                    print(f"❌ Root endpoint failed: {response.status}")
                    return False

            # Test Claude endpoint
            print("\n💬 Testing Claude endpoint...")
            chat_request = {
                "prompt": "API service test - respond with 'DIRECT_API_SUCCESS'",
                "model": "sonnet",
                "timeout": 30,
            }

            async with session.post(
                f"{base_url}/claude", json=chat_request
            ) as response:
                if response.status == 200:
                    chat_result = await response.json()
                    print("✅ Claude endpoint successful:")
                    print(f"Response: {chat_result['response']}")

                    if "DIRECT_API_SUCCESS" in chat_result["response"]:
                        print("🎯 Generic Claude API integration working!")
                        return True
                    else:
                        print("⚠️  Unexpected response content")
                        return False
                else:
                    error_text = await response.text()
                    print(f"❌ Claude endpoint failed: {response.status}")
                    print(f"Error: {error_text}")
                    return False

    except Exception as e:
        print(f"❌ API service endpoints test failed: {e}")
        return False


async def main():
    """Run all integration tests"""
    print("🚀 Claude API Service Integration Tests")
    print("=" * 50)

    tests = [
        ("Provider Integration", test_provider_integration),
        ("API Service Endpoints", test_api_service_endpoints),
        ("Pydantic Agent Integration", test_pydantic_agent_integration),
        ("Scribe Integration", test_scribe_integration),
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

    print("\n" + "=" * 50)
    print("INTEGRATION TEST RESULTS:")
    print("=" * 50)

    all_passed = True
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name}: {status}")
        if not success:
            all_passed = False

    print(
        f"\nOverall: {'🎉 ALL TESTS PASSED' if all_passed else '⚠️  SOME TESTS FAILED'}"
    )

    if all_passed:
        print("\n🎯 The Claude API Service integration is working correctly!")
        print(
            "   MaxSubscriptionProvider should now work without nested subprocess issues."
        )
    else:
        print("\n🔧 Integration issues detected. Check the error messages above.")
        print("   Ensure:")
        print("   1. Claude API service is running: docker-compose up -d")
        print("   2. Claude CLI has Max subscription access")
        print("   3. All dependencies are installed")


if __name__ == "__main__":
    asyncio.run(main())
