#!/usr/bin/env python3
"""
Test runner for voicemidi package.
This script provides a simple interface to run all tests or specific test files.
"""

import argparse
import os
import subprocess
import sys


def list_test_files():
    """List all test files in the tests directory."""
    test_files = [f for f in os.listdir(os.path.dirname(__file__)) 
                  if f.startswith("test_") and f.endswith(".py")]
    return sorted(test_files)


def run_single_test(test_file, args=[]):
    """Run a single test file with optional arguments."""
    print(f"\n=== Running {test_file} ===")
    
    test_path = os.path.join(os.path.dirname(__file__), test_file)
    cmd = [sys.executable, test_path] + args
    
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Run tests for the voicemidi package")
    parser.add_argument("test", nargs="?", help="Specific test file to run (without .py extension)")
    parser.add_argument("--list", action="store_true", help="List available test files")
    parser.add_argument("--args", nargs=argparse.REMAINDER, 
                        help="Additional arguments to pass to the test script")
    
    args = parser.parse_args()
    test_files = list_test_files()
    
    if args.list:
        print("Available test files:")
        for test_file in test_files:
            print(f"  {test_file}")
        return 0
    
    if args.test:
        test_file = f"test_{args.test}.py" if not args.test.startswith("test_") else f"{args.test}.py"
        if test_file in test_files:
            success = run_single_test(test_file, args.args or [])
            return 0 if success else 1
        else:
            print(f"Error: Test file '{test_file}' not found")
            return 1
    
    # Run all tests
    print(f"Running {len(test_files)} test files...")
    
    success = True
    for test_file in test_files:
        if test_file != "run_tests.py" and test_file.endswith(".py"):
            if not run_single_test(test_file, ["--help"]):
                success = False
    
    if success:
        print("\nAll tests completed successfully!")
    else:
        print("\nSome tests failed!")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 