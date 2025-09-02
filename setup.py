#!/usr/bin/env python3
"""
Setup script for Moment Catcher
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install Python requirements."""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_ffmpeg():
    """Check if FFmpeg is installed."""
    try:
        subprocess.check_call(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ FFmpeg is installed!")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg is not installed or not in PATH.")
        print_ffmpeg_instructions()
        return False

def print_ffmpeg_instructions():
    """Print FFmpeg installation instructions."""
    system = platform.system().lower()
    
    print("\n📋 FFmpeg Installation Instructions:")
    print("=" * 50)
    
    if system == "linux":
        print("Ubuntu/Debian:")
        print("  sudo apt update")
        print("  sudo apt install ffmpeg")
        print("\nCentOS/RHEL:")
        print("  sudo yum install ffmpeg")
        print("  # or")
        print("  sudo dnf install ffmpeg")
    elif system == "darwin":
        print("macOS:")
        print("  brew install ffmpeg")
        print("\nOr download from: https://ffmpeg.org/download.html")
    elif system == "windows":
        print("Windows:")
        print("  1. Download from: https://ffmpeg.org/download.html")
        print("  2. Extract to a folder (e.g., C:\\ffmpeg)")
        print("  3. Add C:\\ffmpeg\\bin to your PATH environment variable")
    else:
        print("Please visit: https://ffmpeg.org/download.html")

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    directories = ["uploads", "outputs", "static/css", "static/js", "templates"]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  ✅ Created: {directory}/")
    
    return True

def main():
    """Main setup function."""
    print("🎬 Moment Catcher Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        print("❌ Failed to create directories")
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install Python dependencies")
        sys.exit(1)
    
    # Check FFmpeg
    ffmpeg_ok = check_ffmpeg()
    
    print("\n" + "=" * 50)
    if ffmpeg_ok:
        print("🎉 Setup completed successfully!")
        print("\nTo run the application:")
        print("  python app.py")
        print("\nThen open your browser to: http://localhost:5000")
    else:
        print("⚠️  Setup completed with warnings.")
        print("Please install FFmpeg before running the application.")
        print("\nAfter installing FFmpeg, run:")
        print("  python app.py")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()