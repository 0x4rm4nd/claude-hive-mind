#!/usr/bin/env python3
"""
Run All Max Subscription Tests
==============================
Convenience script to run all test files in sequence.
"""

import subprocess
import sys
from pathlib import Path

def run_test(test_file):
    """Run a single test file and return success status"""
    print(f"\n{'='*60}")
    print(f"🚀 RUNNING: {test_file}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ ERROR running {test_file}: {e}")
        return False

def main():
    """Run all test files"""
    test_dir = Path(__file__).parent
    test_files = [
        test_dir / "test_max_subscription.py",
        test_dir / "test_enhanced_monkey_patch.py"
    ]
    
    print("🧪 Max Subscription Provider - Test Suite")
    print("=" * 45)
    
    results = {}
    for test_file in test_files:
        if test_file.exists():
            results[test_file.name] = run_test(str(test_file))
        else:
            print(f"⚠️  Test file not found: {test_file}")
            results[test_file.name] = False
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST RESULTS SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())