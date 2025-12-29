#!/usr/bin/env python
"""
Career Compass Setup Verification Script
Verifies that all components are properly installed and configured
"""

import os
import sys
import django
from pathlib import Path

def check_django_setup():
    """Check Django installation and configuration"""
    print("🔍 Checking Django Setup...")
    
    # Check if Django is installed
    try:
        import django
        print(f"✅ Django {django.get_version()} installed")
    except ImportError:
        print("❌ Django not installed - run: pip install -r requirements.txt")
        return False
    
    # Check if project settings are available
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
        django.setup()
        print("✅ Django settings configured")
    except Exception as e:
        print(f"❌ Django settings error: {e}")
        return False
    
    return True

def check_database():
    """Check database and models"""
    print("\n🔍 Checking Database...")
    
    try:
        from django.core.management import call_command
        from main.models import Profile, Conversation, Message, Recommendation, InterviewAttempt, Resume, CoverLetter
        
        # Check if tables exist
        from django.db import connection
        tables = connection.introspection.table_names()
        
        required_tables = [
            'main_profile', 'main_conversation', 'main_message',
            'main_recommendation', 'main_interviewattempt', 
            'main_resume', 'main_coverletter'
        ]
        
        missing_tables = [t for t in required_tables if t not in tables]
        
        if missing_tables:
            print(f"⚠️  Missing database tables: {missing_tables}")
            print("   Run: python manage.py migrate")
            return False
        
        print("✅ All database tables present")
        print(f"   - Profile: Ready")
        print(f"   - Conversation: Ready")
        print(f"   - Message: Ready")
        print(f"   - Recommendation: Ready")
        print(f"   - InterviewAttempt: Ready")
        print(f"   - Resume: Ready")
        print(f"   - CoverLetter: Ready")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    return True

def check_dependencies():
    """Check required Python packages"""
    print("\n🔍 Checking Dependencies...")
    
    required_packages = {
        'django': '5.2.8',
        'requests': '2.31.0',
        'reportlab': '4.0.0'
    }
    
    all_ok = True
    for package, version in required_packages.items():
        try:
            module = __import__(package)
            if hasattr(module, '__version__'):
                print(f"✅ {package} ({module.__version__})")
            else:
                print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} not installed - run: pip install {package}")
            all_ok = False
    
    return all_ok

def check_static_files():
    """Check static files and templates"""
    print("\n🔍 Checking Templates...")
    
    template_files = [
        'templates/main/base.html',
        'templates/main/index.html',
        'templates/main/chat.html',
        'templates/main/recommendations.html',
        'templates/main/interview.html',
        'templates/main/resume.html',
        'templates/main/cover_letter.html',
    ]
    
    all_ok = True
    for template in template_files:
        path = Path(template)
        if path.exists():
            print(f"✅ {template}")
        else:
            print(f"❌ {template} - NOT FOUND")
            all_ok = False
    
    return all_ok

def check_ollama():
    """Check Ollama connectivity"""
    print("\n🔍 Checking Ollama Integration...")
    
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=2)
        if response.status_code == 200:
            print("✅ Ollama service is running at http://localhost:11434")
            models = response.json().get('models', [])
            if models:
                model_names = [m.get('name') for m in models]
                print(f"✅ Available models: {', '.join(model_names)}")
                if any('mistral' in m.lower() for m in model_names):
                    print("✅ Mistral model is installed")
                else:
                    print("⚠️  Mistral model not found - run: ollama pull mistral")
            else:
                print("⚠️  No models found - run: ollama pull mistral")
        else:
            print(f"⚠️  Ollama responded with status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("⚠️  Ollama not running - start with: ollama serve")
    except Exception as e:
        print(f"⚠️  Ollama check failed: {e}")
    
    return True

def main():
    """Run all verification checks"""
    print("\n" + "="*60)
    print("🚀 CAREER COMPASS - SETUP VERIFICATION")
    print("="*60)
    
    checks = [
        ("Django Setup", check_django_setup),
        ("Dependencies", check_dependencies),
        ("Templates", check_static_files),
        ("Database", check_database),
        ("Ollama Integration", check_ollama),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 VERIFICATION SUMMARY")
    print("="*60)
    
    for name, result in results:
        status = "✅ PASS" if result else "⚠️  NEEDS ATTENTION"
        print(f"{status} - {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - Ready to run!")
        print("\nStart the development server:")
        print("  python manage.py runserver")
        print("\nAccess the application at:")
        print("  http://127.0.0.1:8000/")
    else:
        print("⚠️  Some checks need attention - see above for details")
        print("\nCommon fixes:")
        print("  1. Run migrations: python manage.py migrate")
        print("  2. Install dependencies: pip install -r requirements.txt")
        print("  3. Start Ollama: ollama serve (in new terminal)")
        print("  4. Pull Mistral: ollama pull mistral")
    
    print("="*60 + "\n")
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
