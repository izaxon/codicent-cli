#!/usr/bin/env python3
"""
Test runner script for the Codicent CLI project.
"""

import subprocess
import sys
import os

def run_tests():
    """Run the test suite."""
    print("🧪 Running Codicent CLI test suite...")
    print("=" * 50)
    
    try:
        # Use unittest directly since pytest has issues on this system
        result = subprocess.run([sys.executable, "test_app.py"], 
                              capture_output=False, cwd=os.path.dirname(__file__))
        if result.returncode == 0:
            print("✅ All unit tests passed")
            return True
        else:
            print("❌ Some unit tests failed")
            return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def run_help_test():
    """Test help functionality."""
    print("\n🔧 Testing CLI help functionality...")
    print("-" * 50)
    
    try:
        result = subprocess.run([sys.executable, "app.py", "--help"], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        if result.returncode == 0 and "Codicent CLI" in result.stdout:
            print("✅ Help functionality works")
            return True
        else:
            print("❌ Help functionality failed")
            return False
    except Exception as e:
        print(f"❌ Error testing help: {e}")
        return False

def run_version_test():
    """Test version functionality."""
    print("\n📋 Testing CLI version functionality...")
    print("-" * 50)
    
    try:
        result = subprocess.run([sys.executable, "app.py", "--version"], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        if result.returncode == 0 and "v0.4.3" in result.stdout:
            print("✅ Version functionality works")
            return True
        else:
            print("❌ Version functionality failed")
            return False
    except Exception as e:
        print(f"❌ Error testing version: {e}")
        return False

def main():
    """Main test runner."""
    print("🚀 Codicent CLI Test Runner")
    print("=" * 50)
    
    success = True
    
    # Run unit tests
    if not run_tests():
        success = False
    
    # Run CLI tests
    if not run_help_test():
        success = False
    
    if not run_version_test():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
