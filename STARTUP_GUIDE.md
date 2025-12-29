# 🚀 Career Compass - Quick Start Guide

## Prerequisites
- Python 3.9+ installed
- Windows PowerShell
- Ollama installed (https://ollama.ai)

## ⚡ Quick Start (5 Minutes)

### Step 1: Activate Virtual Environment
```powershell
cd "P:\Desktop\PROJEcTS\CAREER"
.venv\Scripts\Activate.ps1
```
You should see `(.venv)` at the beginning of your PowerShell prompt.

### Step 2: Verify Setup (Optional)
```powershell
python test_setup.py
```
This checks that all components are installed and configured.

### Step 3: Start Ollama (In a NEW Terminal)
```powershell
ollama serve
```
This must be running for AI features to work. Keep this terminal open.

### Step 4: Pull Mistral Model (Run Once)
In another new PowerShell terminal:
```powershell
ollama pull mistral
```
This downloads the Mistral 7B model (~5GB). Only needed once.

### Step 5: Start Django Dev Server
```powershell
cd "P:\Desktop\PROJEcTS\CAREER"
.venv\Scripts\Activate.ps1
python manage.py runserver
```

### Step 6: Open Browser
Navigate to: **http://127.0.0.1:8000/**

---

## 📋 Full Terminal Setup

You'll need **3 separate PowerShell terminals** running simultaneously:

### Terminal 1: Ollama Service (Keep Running)
```powershell
ollama serve
```
Output will show:
```
Ollama is running on http://localhost:11434
```

### Terminal 2: Ollama Models (One-Time Setup)
```powershell
ollama pull mistral
```
Wait for download to complete (~5GB).

### Terminal 3: Django Development Server
```powershell
cd "P:\Desktop\PROJEcTS\CAREER"
.venv\Scripts\Activate.ps1
python manage.py runserver
```
Output will show:
```
Django version 5.2.8
Starting development server at http://127.0.0.1:8000/
```

---

## 🌐 Access the Application

| Component | URL |
|-----------|-----|
| **Main Site** | http://127.0.0.1:8000/ |
| **Chat** | http://127.0.0.1:8000/chat/ |
| **Recommendations** | http://127.0.0.1:8000/recommendations/ |
| **Mock Interview** | http://127.0.0.1:8000/interview/ |
| **Resume Builder** | http://127.0.0.1:8000/resume/ |
| **Cover Letter** | http://127.0.0.1:8000/cover-letter/ |
| **Admin Panel** | http://127.0.0.1:8000/admin/ |

---

## 🔑 Admin Access

To access the admin panel (`/admin/`):

1. Create an admin user (one-time setup):
```powershell
python manage.py createsuperuser
```
Follow the prompts to set username and password.

2. Login at http://127.0.0.1:8000/admin/ with your credentials.

---

## 🧪 Testing Features

### 1. Chat Feature (Quick Test - 30 seconds)
1. Go to http://127.0.0.1:8000/chat/
2. Type: "What are the top 5 most in-demand tech skills right now?"
3. Wait for AI response (10-30 seconds on first call)
4. Your conversation appears in the sidebar

### 2. Career Recommendations (1 minute)
1. Go to http://127.0.0.1:8000/recommendations/
2. Fill in the form:
   - Name: Your Name
   - Education: Bachelor's
   - Experience: 5 (years)
   - Skills: Python, JavaScript, SQL
3. Click Submit
4. View your personalized recommendations

### 3. Mock Interview (2 minutes)
1. Go to http://127.0.0.1:8000/interview/
2. Select role: "Data Scientist"
3. Choose 5 questions
4. Ollama generates role-specific questions
5. Type your answers and submit

### 4. Resume Builder (3 minutes)
1. Go to http://127.0.0.1:8000/resume/
2. Fill in all sections with your info
3. Click "Save Resume & Download JSON"
4. Your resume data is saved to database

### 5. Cover Letter Generator (2 minutes)
1. Go to http://127.0.0.1:8000/cover-letter/
2. Fill in:
   - Name: Your Name
   - Role: Software Developer
   - Company: Tech Company Inc
3. Click "Generate Cover Letter"
4. AI creates your cover letter
5. Click "Copy to Clipboard"

---

## ⚠️ Troubleshooting

### "Cannot connect to Ollama" Error
**Problem:** Chat/Interview/Cover Letter not working
**Solution:** 
1. Open a new PowerShell terminal
2. Run `ollama serve`
3. Wait for "Ollama is running on http://localhost:11434"
4. Retry your request

### "Port 8000 Already in Use"
**Problem:** Django won't start
**Solution:** 
```powershell
python manage.py runserver 8001
```
Then access at http://127.0.0.1:8001/

### Virtual Environment Not Activated
**Problem:** Commands not recognized
**Solution:**
```powershell
.venv\Scripts\Activate.ps1
```
Look for `(.venv)` in your prompt.

### Database Errors
**Problem:** Tables not found
**Solution:**
```powershell
python manage.py migrate
```

### Slow First Response
**Normal behavior** - First Ollama call takes 10-30 seconds as the model loads into memory. Subsequent calls are faster (2-5 seconds).

---

## 📊 System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|------------|
| **RAM** | 4GB | 8GB+ |
| **Disk Space** | 6GB | 10GB+ |
| **CPU** | Dual-core | Quad-core+ |
| **Network** | Not required | N/A |

---

## 🎯 Features Overview

### ✅ Chat Assistant
- Real-time conversations with AI
- Persistent conversation history
- Perfect for career questions

### ✅ Career Recommendations
- AI-powered role suggestions
- Skill-to-role matching
- Market trend indicators

### ✅ Mock Interview
- 20+ practice roles
- AI-generated questions
- Performance feedback

### ✅ Resume Builder
- Professional form fields
- Multiple sections
- JSON export

### ✅ Cover Letter Generator
- Personalized generation
- Copy to clipboard
- Database storage

---

## 🛑 Stopping the Application

When finished:

1. **Stop Django Server:** Press `Ctrl+C` in Terminal 3
2. **Stop Ollama:** Press `Ctrl+C` in Terminal 1
3. **Deactivate venv:** Type `deactivate`

---

## 📚 Next Steps

After everything is running:

1. **Explore Features:** Try each feature on the home page
2. **Admin Panel:** View data in `/admin/`
3. **Customize:** Modify templates in `templates/main/`
4. **Enhance:** Add new features to `main/views.py`

---

## 🆘 Need Help?

### Check Django is Working
```powershell
python manage.py check
```
Should output: `System check identified no issues (0 silenced).`

### Check Database
```powershell
python manage.py dbshell
```
Type `.tables` to see all tables.

### View Django Logs
Django logs appear in Terminal 3. Look for error messages there.

### Verify Ollama Connection
```powershell
curl http://localhost:11434/api/tags
```
Should return JSON with available models.

---

## 💡 Pro Tips

1. **Keep all 3 terminals visible** - Makes troubleshooting easier
2. **Use Ctrl+Shift+Esc to kill stuck Python** - If a process hangs
3. **Clear browser cache** - If seeing old versions of pages
4. **Check Django logs** - Error messages appear in Terminal 3
5. **Wait for Ollama first call** - First response takes 10-30 seconds

---

## 📝 Quick Commands Reference

```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Start development server
python manage.py runserver

# Create database tables
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Check for issues
python manage.py check

# Run tests
python manage.py test

# Start Ollama (separate terminal)
ollama serve

# Download model (separate terminal)
ollama pull mistral

# Check Ollama status
curl http://localhost:11434/api/tags
```

---

## 🎉 You're Ready!

Everything is set up. Start with these 3 commands in separate terminals:

```powershell
# Terminal 1
ollama serve

# Terminal 2
cd "P:\Desktop\PROJEcTS\CAREER"; .venv\Scripts\Activate.ps1; python manage.py runserver

# Then open browser to: http://127.0.0.1:8000/
```

**Happy career planning!** 🚀
