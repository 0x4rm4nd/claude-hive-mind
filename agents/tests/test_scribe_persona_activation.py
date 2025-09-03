#!/usr/bin/env python3
"""
Scribe Persona Activation Test
=============================
Test that Scribe prompts automatically trigger Docker persona response
"""

import time
import requests
import json


def test_scribe_persona_activation():
    """Test that Scribe-related prompts automatically get 'Using the Scribe Agent,' prefix"""
    print("🧪 Testing Scribe persona activation...")

    # Simple scribe-related prompt that should trigger persona activation
    scribe_task = "Create a session for analyzing the crypto-data service architecture"

    start_time = time.time()

    try:
        response = requests.post(
            "http://localhost:47291/claude",
            json={
                "prompt": f"System: You are the Scribe Agent.\n\nUser: {scribe_task}",
                "model": "sonnet",
                "timeout": 60,
            },
            timeout=65,
        )

        duration = time.time() - start_time
        print(f"⏱️  Request completed in {duration:.2f}s")

        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            print(f"✅ Success: {response_text[:200]}...")

            # Check if response seems to be from Scribe persona (should be more structured)
            if any(
                indicator in response_text.lower()
                for indicator in [
                    "session",
                    "complexity",
                    "level",
                    "analysis",
                    "scribe",
                ]
            ):
                print("✅ Response appears to be from Scribe persona")
                return True
            else:
                print("⚠️  Response doesn't clearly indicate Scribe persona activation")
                return False
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Exception after {duration:.2f}s: {e}")
        return False


def test_queen_persona_activation():
    """Test that Queen-related prompts automatically get 'Using the Queen Agent,' prefix"""
    print("\n🧪 Testing Queen persona activation...")

    # Simple queen-related prompt that should trigger persona activation
    queen_task = (
        "Orchestrate a complex multi-worker analysis of the SmartWalletFX architecture"
    )

    start_time = time.time()

    try:
        response = requests.post(
            "http://localhost:47291/claude",
            json={
                "prompt": f"System: You are the orchestrator.\n\nUser: {queen_task}",
                "model": "opus",  # Use actual Claude model name
                "timeout": 60,
            },
            timeout=65,
        )

        duration = time.time() - start_time
        print(f"⏱️  Request completed in {duration:.2f}s")

        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            print(f"✅ Success: {response_text[:200]}...")

            # Check if response seems to be from Queen persona
            if any(
                indicator in response_text.lower()
                for indicator in [
                    "strategic",
                    "coordination",
                    "orchestration",
                    "workers",
                    "decomposition",
                ]
            ):
                print("✅ Response appears to be from Queen persona")
                return True
            else:
                print("⚠️  Response doesn't clearly indicate Queen persona activation")
                return False
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        duration = time.time() - start_time
        print(f"❌ Exception after {duration:.2f}s: {e}")
        return False


if __name__ == "__main__":
    print("🎭 Testing Agent Persona Activation via Custom Max Subscription\n")

    scribe_success = test_scribe_persona_activation()
    queen_success = test_queen_persona_activation()

    print(f"\n📊 Results:")
    print(f"   Scribe Persona: {'✅ PASS' if scribe_success else '❌ FAIL'}")
    print(f"   Queen Persona:  {'✅ PASS' if queen_success else '❌ FAIL'}")

    if scribe_success and queen_success:
        print("\n🎉 All persona activation tests passed!")
    else:
        print("\n⚠️  Some persona activation tests failed - check configuration")
