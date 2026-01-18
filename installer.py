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
            # Try installing without --break-system-packages first
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"  ✓ {package} installed")
            installed.append(package)
        except subprocess.CalledProcessError:
            try:
                # If that fails, try with --user flag
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package, "--user", "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"  ✓ {package} installed (user install)")
                installed.append(package)
            except subprocess.CalledProcessError:
                print(f"  ✗ Failed to install {package}")
                failed.append(package)
    
    print()
    return installed, failed

def create_desktop_shortcut():
    print("Creating shortcuts...")
    system = platform.system()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if system == "Windows":
        try:
            import winshell
            from win32com.client import Dispatch
            
            desktop = winshell.desktop()
            path = os.path.join(desktop, "Plagiarism Checker.lnk")
            target = os.path.join(script_dir, "run.bat")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = script_dir
            shortcut.IconLocation = target
            shortcut.save()
            
            print("✓ Desktop shortcut created")
            return True
        except ImportError:
            print("⚠ Could not create desktop shortcut (winshell/pywin32 not available)")
            print("  Install with: pip install winshell pywin32")
            print("  You can manually create a shortcut to run.bat")
            return False
        except Exception as e:
            print(f"⚠ Could not create desktop shortcut: {e}")
            print("  You can manually create a shortcut to run.bat")
            return False
    elif system == "Linux":
        try:
            desktop_file = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Plagiarism Checker
Comment=Academic Integrity Tool
Exec={sys.executable} {os.path.join(script_dir, 'main.py')}
Path={script_dir}
Terminal=false
Categories=Education;Office;
"""
            desktop_path = os.path.expanduser("~/Desktop/plagiarism-checker.desktop")
            with open(desktop_path, 'w') as f:
                f.write(desktop_file)
            os.chmod(desktop_path, 0o755)
            print("✓ Desktop shortcut created")
            return True
        except:
            print("⚠ Could not create desktop shortcut")
            return False
    
    elif system == "Darwin":
        print("⚠ Automatic shortcut creation not available on macOS")
        print("  Run: ./run.sh")
        return False
    
    return False

def main():
    """Main installation function"""
    print_header()
    if not check_python():
        print("\n⚠ Installation cannot continue.")
        input("Press Enter to exit...")
        return
    if not check_tkinter():
        print("\n⚠ Installation cannot continue.")
        input("Press Enter to exit...")
        return
    
    print("\nTesting basic functionality...")
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from main import PlagiarismEngine
        engine = PlagiarismEngine()
        print("✓ Core functionality test passed")
    except Exception as e:
        print(f"⚠ Core functionality test failed: {e}")
        print("  The application may not work properly")
    
    installed, failed = install_dependencies()
    create_desktop_shortcut()
    print()
    print("=" * 70)
    print("INSTALLATION COMPLETE")
    print("=" * 70)
    
    if installed:
        print("✓ Successfully installed packages:")
        for package in installed:
            print(f"  - {package}")
    
    if failed:
        print("⚠ Failed to install packages:")
        for package in failed:
            print(f"  - {package}")
        print("  Note: The application will work with limited file format support")
    
    print()
    print("You can now run the Plagiarism Checker:")
    system = platform.system()
    if system == "Windows":
        print("  • Double-click the desktop shortcut")
        print("  • Or run: run.bat")
    elif system == "Linux":
        print("  • Double-click the desktop shortcut")
        print("  • Or run: ./run.sh")
    elif system == "Darwin":
        print("  • Run: ./run.sh")
    
    print(f"  • Or run: python {os.path.join(os.path.dirname(__file__), 'main.py')}")
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user.")
    except Exception as e:
        print(f"\n\nError during installation: {e}")
        input("\nPress Enter to exit...")