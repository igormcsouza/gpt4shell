#!/usr/bin/env python3
"""
Test runner for gpt4shell unit tests with coverage reporting.

This script runs all unit tests for the gpt4shell project and provides
coverage reporting using pytest-cov.

Usage:
    python run_tests.py          # Run all tests with coverage
    poetry run python run_tests.py  # Run with Poetry environment (recommended)
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are available."""
    try:
        import langchain_core
        import langchain_openai
        import rich
        import pytest
        import pytest_cov
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📋 Please ensure all dependencies are installed.")
        print("🔧 Run: poetry install")
        print("🚀 Then run: poetry run python run_tests.py")
        return False
    return True

if __name__ == '__main__':
    print("🧪 GPT4Shell Test Suite with Coverage")
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
    
    print("🔍 Running tests with coverage...")
    print()
    
    # Run pytest with coverage
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest'
        ], check=False)
        
        print()
        print("=" * 50)
        if result.returncode == 0:
            print("✅ All tests passed!")
            print("📊 Coverage report generated in htmlcov/ directory")
        else:
            print("❌ Some tests failed or coverage threshold not met!")
        
        # Exit with the same code as pytest
        sys.exit(result.returncode)
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)