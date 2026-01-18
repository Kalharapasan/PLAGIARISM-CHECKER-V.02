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

def check_tkinter():
    print("Checking Tkinter (GUI library)...")
    try:
        import tkinter
        print("✓ Tkinter is available")
        return True
    except ImportError:
        print("✗ Tkinter is not installed")
        print()
        
        system = platform.system()
        if system == "Linux":
            print("Install with:")
            print("  Ubuntu/Debian: sudo apt-get install python3-tk")
            print("  Fedora: sudo dnf install python3-tkinter")
        elif system == "Darwin":
            print("Tkinter should be included with Python on macOS")
            print("Try reinstalling Python from python.org")
        elif system == "Windows":
            print("Tkinter should be included with Python on Windows")
            print("Try reinstalling Python from python.org")
        
        return False

def install_dependencies():
    print()
    print("Installing optional dependencies...")
    print("(This enables support for DOCX and PDF files)")
    print()
    
    packages = {
        'python-docx': 'Microsoft Word (.docx) support',
        'pypdf': 'PDF support (basic)',
        'pdfplumber': 'PDF support (advanced, with tables)'
    }
    
    installed = []
    failed = []
    
    for package, description in packages.items():
        print(f"Installing {package} ({description})...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "--break-system-packages", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"  ✓ {package} installed")
            installed.append(package)
        except subprocess.CalledProcessError:
            print(f"  ✗ Failed to install {package}")
            failed.append(package)
    
    print()
    return installed, failed