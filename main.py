"""
Azure App Service entry point for Streamlit application.
This wrapper helps ensure proper startup on Azure.
"""
import subprocess
import sys
import os

def main():
    # Ensure we're using the correct Python interpreter
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    
    # Set environment variables if not set
    os.environ.setdefault('PORT', '8000')
    
    # Run streamlit
    cmd = [
        sys.executable,
        '-m',
        'streamlit',
        'run',
        'app.py',
        '--server.port=' + os.environ.get('PORT', '8000'),
        '--server.address=0.0.0.0',
        '--logger.level=info'
    ]
    
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd)

if __name__ == '__main__':
    main()
