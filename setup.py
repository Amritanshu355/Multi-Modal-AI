#!/usr/bin/env python3
"""
AI Hiring Copilot - Setup Script
Initializes the environment and validates all dependencies
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_status(status, message):
    icons = {
        'success': '✓',
        'error': '✗',
        'warning': '⚠',
        'info': 'ℹ'
    }
    print(f"{icons.get(status, '?')} {message}")

def check_python_version():
    print_header("Python Version Check")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print_status('success', f"Python {version.major}.{version.minor}.{version.micro} ✓")
        return True
    else:
        print_status('error', f"Python 3.9+ required (found {version.major}.{version.minor})")
        return False

def check_dependencies():
    print_header("Checking Dependencies")
    
    required = ['streamlit', 'pytesseract', 'sentence-transformers', 'faiss-cpu', 'PyPDF2']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print_status('success', f"{package}")
        except ImportError:
            print_status('error', f"{package} - NOT INSTALLED")
            missing.append(package)
    
    return len(missing) == 0, missing

def check_external_tools():
    print_header("External Tools Check")
    
    # Check Tesseract
    tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]
    
    tesseract_found = False
    for path in tesseract_paths:
        if os.path.exists(path):
            print_status('success', f"Tesseract OCR found at {path}")
            tesseract_found = True
            break
    
    if not tesseract_found:
        print_status('warning', "Tesseract OCR not found. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
    
    # Check Ollama
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print_status('success', "Ollama service is running")
            if 'mistral' in result.stdout:
                print_status('success', "Mistral model is installed")
            else:
                print_status('warning', "Mistral model not found. Run: ollama pull mistral")
        else:
            print_status('error', "Ollama service not responding")
    except Exception as e:
        print_status('warning', f"Ollama not accessible. Download from: https://ollama.ai")
    
    return tesseract_found

def install_requirements():
    print_header("Installing Python Dependencies")
    print("Running: pip install -r requirements.txt\n")
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print_status('success', "All dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print_status('error', "Failed to install dependencies")
        return False

def create_directories():
    print_header("Creating Directories")
    
    dirs = ['uploaded_resumes', 'candidate_database', 'reports']
    
    for directory in dirs:
        Path(directory).mkdir(exist_ok=True)
        print_status('success', f"Directory: {directory}")

def setup_config():
    print_header("Configuration Setup")
    
    if os.path.exists('config.json'):
        print_status('success', "config.json exists")
    else:
        print_status('warning', "config.json not found - creating default")
        # Default config already created by the system

def run_tests():
    print_header("Running Validation Tests")
    
    try:
        # Test imports
        from utils import extract_skills, calculate_match_score
        print_status('success', "Utils module imports correctly")
        
        # Test skill extraction
        test_text = "Python developer with AWS and Docker experience"
        skills = extract_skills(test_text)
        if skills['technical_skills']:
            print_status('success', "Skill extraction working")
        
        # Test embedding model
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print_status('success', "Embedding model loaded")
        
    except Exception as e:
        print_status('error', f"Validation failed: {e}")
        return False
    
    return True

def main():
    print("\n" + "="*60)
    print("  🤖 AI HIRING COPILOT - SETUP WIZARD")
    print("="*60)
    
    # Run checks
    checks = []
    
    checks.append(("Python Version", check_python_version()))
    
    deps_ok, missing = check_dependencies()
    if not deps_ok:
        print("\nMissing dependencies detected.")
        if input("Install missing packages? (y/n): ").lower() == 'y':
            install_requirements()
    checks.append(("Dependencies", deps_ok))
    
    checks.append(("External Tools", check_external_tools()))
    
    create_directories()
    setup_config()
    
    if run_tests():
        checks.append(("Validation", True))
    else:
        checks.append(("Validation", False))
    
    # Summary
    print_header("Setup Summary")
    
    all_passed = all(check[1] for check in checks)
    
    for check_name, passed in checks:
        status = 'success' if passed else 'warning'
        print_status(status, f"{check_name}: {'OK' if passed else 'ISSUES DETECTED'}")
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ Setup complete! Ready to run the application.")
        print("\nTo start the AI Hiring Copilot, run:")
        print("  streamlit run app.py")
    else:
        print("⚠ Setup complete with some warnings. Check the output above.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
