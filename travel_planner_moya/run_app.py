"""
Simple script to run the Travel Planner application
"""

import subprocess
import sys
import os

def check_and_install_requirements():
    """Check if requirements are installed and install if needed"""
    try:
        import streamlit
        import dotenv
        print("✅ All required packages are already installed.")
    except ImportError:
        print("📦 Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")

def run_streamlit_app():
    """Run the Streamlit application"""
    print("🚀 Starting Travel Planner AI...")
    print("🌐 The application will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("\n" + "="*50)
    print("Travel Planner Multi-Agent System")
    print("Powered by MOYA Framework")
    print("="*50)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

if __name__ == "__main__":
    print("🔧 Setting up Travel Planner AI...")
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: main.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install requirements if needed
    check_and_install_requirements()
    
    # Run the application
    run_streamlit_app()
