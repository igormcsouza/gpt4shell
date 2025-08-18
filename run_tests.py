#!/usr/bin/env python3
"""
Test runner for gpt4shell unit tests.

This script runs all unit tests for the gpt4shell project and provides
a convenient way to execute tests during development.

Usage:
    python run_tests.py          # Run all tests
    poetry run python run_tests.py  # Run with Poetry environment (recommended)
"""

import os
import sys
import unittest

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import langchain_core
        import langchain_openai
        import rich
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📋 Please ensure all dependencies are installed.")
        print("🔧 Run: poetry install")
        print("🚀 Then run: poetry run python run_tests.py")
        return False
    return True

if __name__ == '__main__':
    print("🧪 GPT4Shell Test Suite")
    print("=" * 50)
    
    # Check if we're running in Poetry environment
    if 'VIRTUAL_ENV' in os.environ:
        print("✅ Running in virtual environment")
    else:
        print("⚠️  Not running in virtual environment")
        print("💡 Consider using: poetry run python run_tests.py")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("🔍 Discovering and running tests...")
    print()
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    
    # Exit with non-zero code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)