#!/usr/bin/env python3
"""
Test script to verify Moment Catcher installation
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported."""
    required_packages = [
        'cv2',
        'moviepy',
        'numpy',
        'scipy',
        'librosa',
        'sklearn',
        'flask',
        'PIL',
        'matplotlib',
        'seaborn'
    ]
    
    print("🧪 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
                print(f"  ✅ OpenCV: {cv2.__version__}")
            elif package == 'moviepy':
                import moviepy
                print(f"  ✅ MoviePy: {moviepy.__version__}")
            elif package == 'numpy':
                import numpy
                print(f"  ✅ NumPy: {numpy.__version__}")
            elif package == 'scipy':
                import scipy
                print(f"  ✅ SciPy: {scipy.__version__}")
            elif package == 'librosa':
                import librosa
                print(f"  ✅ Librosa: {librosa.__version__}")
            elif package == 'sklearn':
                import sklearn
                print(f"  ✅ Scikit-learn: {sklearn.__version__}")
            elif package == 'flask':
                import flask
                print(f"  ✅ Flask: {flask.__version__}")
            elif package == 'PIL':
                from PIL import Image
                print(f"  ✅ Pillow: {Image.__version__}")
            elif package == 'matplotlib':
                import matplotlib
                print(f"  ✅ Matplotlib: {matplotlib.__version__}")
            elif package == 'seaborn':
                import seaborn
                print(f"  ✅ Seaborn: {seaborn.__version__}")
        except ImportError as e:
            print(f"  ❌ {package}: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0, failed_imports

def test_ffmpeg():
    """Test if FFmpeg is available."""
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ FFmpeg: {version_line}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
        pass
    
    print("  ❌ FFmpeg: Not found or not working")
    return False

def test_directories():
    """Test if required directories exist."""
    import os
    required_dirs = ['uploads', 'outputs', 'templates', 'static']
    
    print("📁 Testing directories...")
    missing_dirs = []
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  ✅ {directory}/")
        else:
            print(f"  ❌ {directory}/ (missing)")
            missing_dirs.append(directory)
    
    return len(missing_dirs) == 0, missing_dirs

def test_app_import():
    """Test if the main app can be imported."""
    try:
        # Test moviepy import first
        try:
            from moviepy.editor import VideoFileClip
        except ImportError:
            from moviepy import VideoFileClip
        
        from app import MomentCatcher, app
        print("  ✅ Main application imports successfully")
        return True
    except ImportError as e:
        print(f"  ❌ Main application: {e}")
        return False

def main():
    """Run all tests."""
    print("🎬 Moment Catcher - Installation Test")
    print("=" * 40)
    
    all_passed = True
    
    # Test imports
    imports_ok, failed_imports = test_imports()
    if not imports_ok:
        all_passed = False
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Run: pip install -r requirements.txt")
    
    # Test FFmpeg
    ffmpeg_ok = test_ffmpeg()
    if not ffmpeg_ok:
        all_passed = False
        print("\n❌ FFmpeg not found. Please install FFmpeg.")
    
    # Test directories
    dirs_ok, missing_dirs = test_directories()
    if not dirs_ok:
        all_passed = False
        print(f"\n❌ Missing directories: {', '.join(missing_dirs)}")
        print("Run: python setup.py")
    
    # Test app import
    app_ok = test_app_import()
    if not app_ok:
        all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! Moment Catcher is ready to use.")
        print("\nTo start the application:")
        print("  python app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\nFor help, see README.md or run:")
        print("  python setup.py")

if __name__ == "__main__":
    main()