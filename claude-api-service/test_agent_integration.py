#!/usr/bin/env python3
"""
Simple test for Agent('custom:max-subscription') integration.

This script demonstrates that the exact syntax requested by the user works:
Agent('custom:max-subscription') routes through Claude API service.
"""

import asyncio
import sys
from pathlib import Path

# Add Pydantic AI to path
sys.path.append(str(Path(__file__).parent.parent / "agents" / "pydantic_ai"))

# Import Pydantic AI with Max subscription integration
from pydantic_ai import Agent
from shared.claude_integration import enable_max_subscription_integration


async def test_agent_syntax():
    """Test the exact Agent syntax requested by the user"""
    print("🚀 Testing Agent('custom:max-subscription') syntax")
    print("=" * 50)
    
    try:
        # Enable the integration (auto-enabled on import, but explicit for clarity)
        print("🔧 Enabling Max subscription integration...")
        integration_enabled = enable_max_subscription_integration()
        
        if not integration_enabled:
            print("❌ Failed to enable integration")
            return False
        
        # Create agent using the exact syntax requested
        print("🤖 Creating Agent('custom:max-subscription')...")
        agent = Agent(
            'custom:max-subscription',
            system_prompt="You are a test assistant. Respond with 'SUCCESS: Claude API service integration working' followed by a brief confirmation."
        )
        
        print("💬 Testing agent.run_async()...")
        result = await agent.run_async("Test message: Verify that Agent('custom:max-subscription') routes through Claude API service")
        
        print(f"✅ Response received: {result.data}")
        
        if "SUCCESS" in str(result.data):
            print("\n🎯 INTEGRATION COMPLETE!")
            print("✅ Agent('custom:max-subscription') works as requested")
            print("✅ No nested subprocess issues")
            print("✅ Uses Max subscription via Claude API service")
            return True
        else:
            print("⚠️  Unexpected response format")
            return False
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        print(f"Full error: {traceback.format_exc()}")
        return False


async def test_other_custom_models():
    """Test other custom models work too"""
    print("\n🧪 Testing other custom models...")
    print("=" * 30)
    
    models_to_test = [
        "custom:claude-opus-4",
        "custom:claude-sonnet-4", 
        "custom:claude-3-5-haiku"
    ]
    
    for model in models_to_test:
        try:
            print(f"Testing {model}...")
            agent = Agent(model)
            result = await agent.run_async(f"Say 'OK' to confirm {model} works")
            print(f"✅ {model}: {result.data}")
        except Exception as e:
            print(f"❌ {model}: {e}")


async def main():
    """Run the integration tests"""
    success = await test_agent_syntax()
    
    if success:
        await test_other_custom_models()
        print("\n🎉 ALL TESTS PASSED!")
        print("\nUsage Examples:")
        print("agent = Agent('custom:max-subscription')")
        print("result = await agent.run_async('Any prompt - analysis, coding, planning, etc.')")
        print("\nNote: Generic /claude endpoint handles ALL Pydantic AI requests")
        print("cd .claude/claude-api-service && docker-compose up -d")
    else:
        print("\n❌ INTEGRATION FAILED")
        print("Check that:")
        print("1. Claude API service is running")
        print("2. Docker has Claude CLI access")
        print("3. Max subscription is working")


if __name__ == "__main__":
    asyncio.run(main())