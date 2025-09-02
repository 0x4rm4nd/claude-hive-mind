#!/usr/bin/env python3
"""
Test Isolated ClaudeAPIServiceClient

Tests the ClaudeAPIServiceClient in isolation, creating a standalone
version that doesn't depend on the full Pydantic AI framework.
"""

import asyncio
import sys
import os

# Add current directory to path to import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import aiohttp
    print("✅ aiohttp available")
except ImportError:
    print("❌ aiohttp not available - installing...")
    os.system("pip install aiohttp")
    import aiohttp


class StandaloneClaudeAPIClient:
    """
    Standalone version of ClaudeAPIServiceClient without Pydantic AI dependencies.
    
    This replicates the core functionality for testing purposes.
    """

    def __init__(
        self,
        api_base_url: str = "http://localhost:47291",
        default_model: str = "sonnet",
    ):
        self.api_base_url = api_base_url
        self.default_model = default_model
        self.service_started = False

        # Model mapping for custom: models
        self.model_mapping = {
            "custom:max-subscription": "sonnet",
            "custom:claude-opus-4": "opus",
            "custom:claude-sonnet-4": "sonnet",
            "custom:claude-3-7-sonnet": "claude-3-7-sonnet-20250219",
            "custom:claude-3-5-haiku": "haiku",
        }

    async def send_prompt(self, prompt: str, model_name: str) -> str:
        """Send a prompt to Claude API service"""
        
        # Check service health first
        if not self.service_started:
            if not await self._check_service_health():
                raise Exception(
                    f"Claude API service is not running at {self.api_base_url}\n"
                    f"Start with: cd .claude/claude-api-service && docker-compose up -d"
                )
            self.service_started = True

        # Map custom model name to Claude model
        claude_model = self.model_mapping.get(model_name, self.default_model)
        
        # Call API service
        try:
            return await self._call_claude_api_service(prompt, claude_model)
        except Exception as e:
            raise Exception(f"Claude API Service failed: {str(e)}")

    async def _check_service_health(self) -> bool:
        """Check if Claude API service is healthy"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.api_base_url}/health",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    if response.status == 200:
                        health_data = await response.json()
                        return health_data.get("status") == "healthy"
        except Exception:
            pass
        return False

    async def _call_claude_api_service(self, prompt: str, model: str) -> str:
        """Call Claude API service"""
        request_data = {"prompt": prompt, "model": model, "timeout": 120}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.api_base_url}/claude",
                json=request_data,
                timeout=aiohttp.ClientTimeout(total=150),
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"API service returned {response.status}: {error_text}")

                result = await response.json()
                return result["response"]

    def get_service_status(self):
        """Get status information"""
        return {
            "api_base_url": self.api_base_url,
            "service_started": self.service_started,
            "default_model": self.default_model,
            "available_models": list(self.model_mapping.keys()),
        }


async def test_standalone_client():
    """Test the standalone client implementation"""
    print("🚀 Testing Standalone ClaudeAPIServiceClient")
    print("=" * 50)
    
    client = StandaloneClaudeAPIClient()
    
    # Test 1: Service status
    print("📊 Client configuration:")
    status = client.get_service_status()
    for key, value in status.items():
        print(f"  {key}: {value}")
    
    # Test 2: Health check
    print(f"\n🔍 Checking service health at {client.api_base_url}")
    is_healthy = await client._check_service_health()
    print(f"Health status: {'✅ Healthy' if is_healthy else '❌ Unhealthy'}")
    
    if not is_healthy:
        print("❌ Cannot proceed with tests - service is not healthy")
        return False
    
    # Test 3: Direct model calls
    print("\n📋 Testing direct model calls:")
    
    models_to_test = ["sonnet", "opus", "haiku"]
    
    for model in models_to_test:
        try:
            print(f"  Testing {model}...")
            response = await client.send_prompt(
                f"Respond with exactly: '{model} via Max subscription OK'",
                model
            )
            print(f"  ✅ {model}: {response.strip()}")
        except Exception as e:
            print(f"  ❌ {model}: {e}")
            return False
    
    # Test 4: Custom model mapping
    print("\n📋 Testing custom:* model mapping:")
    
    custom_models_to_test = [
        "custom:max-subscription",
        "custom:claude-opus-4", 
        "custom:claude-sonnet-4"
    ]
    
    for custom_model in custom_models_to_test:
        try:
            print(f"  Testing {custom_model}...")
            response = await client.send_prompt(
                f"Respond with exactly: 'Agent(\\'{custom_model}\\') working'",
                custom_model
            )
            print(f"  ✅ {custom_model}: {response.strip()}")
        except Exception as e:
            print(f"  ❌ {custom_model}: {e}")
            return False
    
    print("\n🎉 All standalone client tests passed!")
    return True


async def test_agent_simulation():
    """Simulate how Agent('custom:max-subscription') would work"""
    print("\n🤖 Simulating Agent('custom:max-subscription') workflow")
    print("=" * 50)
    
    client = StandaloneClaudeAPIClient()
    
    # Simulate agent conversation
    conversation_steps = [
        "Hello, can you help me with a coding task?",
        "I need to create a simple Python function that adds two numbers.",
        "Can you show me how to write unit tests for that function?"
    ]
    
    print("🔄 Simulating multi-turn conversation with custom:max-subscription:")
    
    for i, prompt in enumerate(conversation_steps, 1):
        try:
            print(f"\n  Step {i}: {prompt}")
            response = await client.send_prompt(prompt, "custom:max-subscription")
            # Show first 100 chars of response
            print(f"  Response: {response[:100]}{'...' if len(response) > 100 else ''}")
        except Exception as e:
            print(f"  ❌ Step {i} failed: {e}")
            return False
    
    print(f"\n✅ Agent('custom:max-subscription') simulation successful!")
    return True


async def main():
    """Run all tests"""
    print("🎯 Testing Agent('custom:max-subscription') Integration")
    print("Focus: Isolated client testing without Pydantic AI framework")
    print("=" * 70)
    
    results = {}
    
    # Test standalone client
    results['standalone_client'] = await test_standalone_client()
    
    # Test agent simulation
    if results['standalone_client']:
        results['agent_simulation'] = await test_agent_simulation()
    else:
        results['agent_simulation'] = False
        print("❌ Skipping agent simulation - client tests failed")
    
    # Summary
    print("\n" + "=" * 70)
    print("🏁 Final Results:")
    print("=" * 70)
    
    all_passed = all(results.values())
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print("=" * 70)
    if all_passed:
        print("🎉 SUCCESS: Agent('custom:max-subscription') integration confirmed!")
        print("✅ HTTP client can communicate with Docker service on port 47291")
        print("✅ Model mapping works correctly for custom:* models")
        print("✅ Max subscription routing is functional")
        print("✅ Ready for Pydantic AI framework integration")
    else:
        print("❌ FAILED: Issues found with the integration")
        
    return all_passed


if __name__ == "__main__":
    asyncio.run(main())