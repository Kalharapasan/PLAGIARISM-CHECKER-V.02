#!/usr/bin/env python3
import os
import sys
import subprocess
import platform

def print_header():
    print("=" * 70)
    print("PLAGIARISM CHECKER - ONE-CLICK INSTALLER")
    print("Desktop Application Setup")
    print("=" * 70)
    print()

def check_python():
    print("Checking Python installation...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("✗ Python 3.7 or higher is required")
        print(f"  Current version: {version.major}.{version.minor}.{version.micro}")
        print("  Please install Python from https://www.python.org/")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True