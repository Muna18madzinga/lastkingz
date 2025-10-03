"""
Setup script for LastKings Liquor Store POS System
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("=" * 60)
    print("LastKings Liquor Store POS System - Setup")
    print("=" * 60)
    print()

    requirements = [
        "pyserial",
    ]

    # Optional: pywin32 for Windows printer support
    if sys.platform == "win32":
        print("Detected Windows system. Installing printer support...")
        requirements.append("pywin32")

    print("Installing required packages...")
    for package in requirements:
        try:
            print(f"  Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"  ✓ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"  ✗ Failed to install {package}")
            print(f"    Please install manually: pip install {package}")

    print()
    print("=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Run 'python sample_products.py' to add sample products")
    print("2. Run 'python pos_system.py' to start the POS system")
    print()

if __name__ == "__main__":
    install_requirements()