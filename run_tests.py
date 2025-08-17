#!/usr/bin/env python3
"""
Test runner for gpt4shell unit tests.

This script runs all unit tests for the gpt4shell project and provides
a convenient way to execute tests during development.
"""

import sys
import unittest

if __name__ == '__main__':
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(0 if result.wasSuccessful() else 1)