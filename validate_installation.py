#!/usr/bin/env python3
"""
Codicent CLI Installation Validator

This script verifies that codicent-cli and all its dependencies
are properly installed and functional.
"""
import sys
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is supported."""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version >= (3, 6):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is supported")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not supported (requires >= 3.6)")
        return False

def check_module_import(module_name, package_name=None):
    """Check if a module can be imported."""
    package_name = package_name or module_name
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            print(f"❌ {package_name} is not installed")
            return False
        
        # Try to actually import it
        module = importlib.import_module(module_name)
        print(f"✅ {package_name} imported successfully")
        
        # Try to get version if available
        if hasattr(module, '__version__'):
            print(f"   Version: {module.__version__}")
        
        return True
    except ImportError as e:
        print(f"❌ Failed to import {package_name}: {e}")
        return False

def check_cli_command():
    """Check if the codicent CLI command is available."""
    print("🔍 Checking CLI command availability...")
    try:
        result = subprocess.run(['codicent', '--help'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and 'Codicent CLI' in result.stdout:
            print("✅ Codicent CLI command is available and working")
            return True
        else:
            print(f"❌ Codicent CLI command failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Codicent CLI command timed out")
        return False
    except FileNotFoundError:
        print("❌ Codicent CLI command not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Error running codicent command: {e}")
        return False

def main():
    """Run all validation checks."""
    print("🚀 Codicent CLI Installation Validator")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("codicent-py", lambda: check_module_import('codicentpy', 'codicent-py')),
        ("rich", lambda: check_module_import('rich')),
        ("prompt_toolkit", lambda: check_module_import('prompt_toolkit')),
        ("requests", lambda: check_module_import('requests')),
        ("CLI Command", check_cli_command),
    ]
    
    passed = 0
    total = len(checks)
    
    for name, check_func in checks:
        print(f"\n🔍 Checking {name}...")
        try:
            if check_func():
                passed += 1
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 All checks passed! Codicent CLI is ready to use.")
        print("💡 Next steps:")
        print("   1. Set your CODICENT_TOKEN environment variable")
        print("   2. Or run 'codicent auth' to authenticate")
        print("   3. Try 'codicent --help' for usage information")
        return 0
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print("💡 Try installing missing dependencies:")
        print("   pip install --upgrade codicent-cli")
        return 1

if __name__ == "__main__":
    sys.exit(main())