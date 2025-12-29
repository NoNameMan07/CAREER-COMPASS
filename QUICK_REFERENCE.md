# 📋 Career Compass - Quick Reference Guide

## 🚀 Common Commands

### Start the Application (3 Terminals)
```powershell
# Terminal 1: Ollama Service
ollama serve

# Terminal 2: Download Model (one-time)
ollama pull mistral

# Terminal 3: Django Server
cd "P:\Desktop\PROJEcTS\CAREER"
.venv\Scripts\Activate.ps1
python manage.py runserver
```

### Activate Virtual Environment
```powershell
.venv\Scripts\Activate.ps1
```

### Deactivate Virtual Environment
```powershell
deactivate
```

### Install New Package
```powershell
pip install package_name
```

### Save Dependencies
```powershell
pip freeze > requirements.txt
```

---

## 🗄️ Database Commands

### Create Database Tables
```powershell
python manage.py migrate
```

### Create Migrations for Model Changes
```powershell
python manage.py makemigrations
```

### Create Admin User
```powershell
python manage.py createsuperuser
```

### Access Database Shell
```powershell
python manage.py dbshell
```

### Reset Database (Warning: Deletes All Data)
```powershell
# Delete db.sqlite3 file
rm db.sqlite3

# Reapply migrations
python manage.py migrate
python manage.py createsuperuser
```

---

## 🛠️ Django Shell

### Start Shell
```powershell
python manage.py shell
```

### View All Users/Profiles
```python
from main.models import Profile
Profile.objects.all()
```

### Create New Profile
```python
from main.models import Profile
Profile.objects.create(
    name="John Doe",
    email="john@example.com",
    location="New York"
)
```

### Query and Update
```python
profile = Profile.objects.get(name="John Doe")
profile.email = "newemail@example.com"
profile.save()
```

### Delete Record
```python
profile = Profile.objects.get(name="John Doe")
profile.delete()
```

### Count Records
```python
Profile.objects.count()
Conversation.objects.count()
```

---

## 📁 File Operations

### List Project Structure
```powershell
tree /F  # Windows tree command
```

### View File Contents
```powershell
Get-Content filename.py
cat filename.py  # Alternative
```

### Create New File
```powershell
New-Item -Path "filename.txt" -Type File
```

### Delete File/Folder
```powershell
Remove-Item filename.txt
Remove-Item -Recurse folder_name  # Delete folder and contents
```

---

## 🔍 Debugging

### Check Django Configuration
```powershell
python manage.py check
```

### View Running Port
```powershell
netstat -ano | findstr :8000
```

### Kill Process on Port
```powershell
Get-Process python | Stop-Process -Force
```

### View Django Logs
Look at Terminal 3 (Django server terminal) for error messages.

### Browser Console
Press `F12` to open developer console.

### Check Ollama Status
```powershell
curl http://localhost:11434/api/tags
```

---

## 🌐 Access Points

| Purpose | URL |
|---------|-----|
| Home | http://127.0.0.1:8000/ |
| Chat | http://127.0.0.1:8000/chat/ |
| Recommendations | http://127.0.0.1:8000/recommendations/ |
| Interview | http://127.0.0.1:8000/interview/ |
| Resume | http://127.0.0.1:8000/resume/ |
| Cover Letter | http://127.0.0.1:8000/cover-letter/ |
| Admin | http://127.0.0.1:8000/admin/ |

---

## 📝 Common Tasks

### Add New Career Role
Edit `main/views.py` - Add to `VALID_CAREER_ROLES` list:
```python
VALID_CAREER_ROLES = [
    # ... existing roles ...
    "Your New Role"
]
```

### Modify Resume Fields
Edit `main/forms.py` - Add to `ResumeForm`:
```python
new_field = forms.CharField(
    label="Field Name",
    widget=forms.TextInput(attrs={'placeholder': 'Enter...'}),
    required=False
)
```

### Update Navbar
Edit `templates/main/base.html` - Modify nav links:
```html
<a href="{% url 'view_name' %}">Link Text</a>
```

### Change Colors/Theme
Edit `templates/main/base.html` - Modify CSS colors:
```css
/* Change purple gradient to different colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add New Page
1. Create view in `main/views.py`
2. Add URL in `main/urls.py`
3. Create template in `templates/main/`
4. Add nav link in `templates/main/base.html`

---

## 🧪 Testing Features

### Test Chat
1. Go to `/chat/`
2. Ask: "What skills do I need for a data scientist?"
3. Wait for response (10-30 seconds first time)

### Test Recommendations
1. Go to `/recommendations/`
2. Fill: Python, Machine Learning, SQL
3. Click Submit
4. View recommendations

### Test Interview
1. Go to `/interview/`
2. Select: "Data Scientist"
3. Choose: 5 questions
4. View generated questions

### Test Resume
1. Go to `/resume/`
2. Fill all fields
3. Click "Save & Download JSON"
4. Download appears

### Test Cover Letter
1. Go to `/cover-letter/`
2. Fill: Name, Role, Company
3. Click "Generate"
4. View and copy letter

---

## 🔐 Security Tips

- ✅ CSRF tokens enabled on all forms
- ✅ Don't share admin URL publicly
- ✅ Use strong admin password
- ✅ Keep Ollama local (no external API)
- ✅ Validate all user inputs
- ✅ Use HTTPS in production

---

## 💾 Backup & Restore

### Backup Database
```powershell
Copy-Item db.sqlite3 db.sqlite3.backup
```

### Restore Database
```powershell
Copy-Item db.sqlite3.backup db.sqlite3
```

### Export Data
```powershell
python manage.py dumpdata > data.json
```

### Import Data
```powershell
python manage.py loaddata data.json
```

---

## 📊 Admin Panel Tasks

### View All Conversations
1. Login to `/admin/`
2. Click "Conversations" in sidebar
3. View all chat sessions
4. Click to edit or delete

### View All Recommendations
1. In Admin, click "Recommendations"
2. View user profiles and roles
3. Use filters to find specific data

### View Interview Attempts
1. In Admin, click "Interview Attempts"
2. View questions (JSON format)
3. View answers (JSON format)
4. View scores

### Manage Resumes
1. In Admin, click "Resumes"
2. View saved resumes
3. Edit or delete as needed

### Search Data
1. In Admin, use search box
2. Search by name, email, role
3. Use filters by date

---

## 🐛 Troubleshooting Checklist

### Ollama Not Working
- [ ] Is `ollama serve` running in Terminal 1?
- [ ] Did you run `ollama pull mistral`?
- [ ] Is port 11434 accessible?
- [ ] Check Task Manager for ollama.exe

### Chat Not Responding
- [ ] Check Ollama is running
- [ ] Wait 10-30 seconds (first load)
- [ ] Check browser console (F12) for errors
- [ ] Check Terminal 3 (Django) for errors

### Database Errors
- [ ] Did you run `python manage.py migrate`?
- [ ] Is db.sqlite3 file present?
- [ ] Check file permissions

### Page Not Loading
- [ ] Did you start Django server?
- [ ] Is correct URL being accessed?
- [ ] Clear browser cache (Ctrl+Shift+Del)

### Admin Won't Load
- [ ] Did you create superuser?
- [ ] Is `/admin/` URL correct?
- [ ] Check login credentials

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Full documentation |
| `STARTUP_GUIDE.md` | Quick start (5 min) |
| `DEVELOPMENT.md` | Developer guide |
| `PROJECT_SUMMARY.md` | Project overview |
| `test_setup.py` | Verification script |
| `QUICK_REFERENCE.md` | This file |

---

## 🎯 Development Workflow

### 1. Start Development Session
```powershell
.venv\Scripts\Activate.ps1
```

### 2. Make Code Changes
Edit files in:
- `main/models.py` - Database models
- `main/views.py` - Application logic
- `main/forms.py` - Form validation
- `templates/main/*.html` - UI pages

### 3. Migrate Changes (if model changes)
```powershell
python manage.py makemigrations
python manage.py migrate
```

### 4. Test Changes
1. Reload browser (F5)
2. Check for errors in Terminal 3
3. Check browser console (F12)

### 5. Commit Changes (if using Git)
```powershell
git add .
git commit -m "Description of changes"
git push
```

---

## 🚀 Performance Tips

1. **First Ollama call takes 10-30 seconds** - Normal, model is loading
2. **Subsequent calls are 2-5 seconds** - Model is cached
3. **Use smaller models if needed** - `ollama pull orca-mini`
4. **Add database indexes** - For large datasets
5. **Use select_related() in queries** - Avoid N+1 queries

---

## 📱 Browser Tools

### DevTools Shortcuts
- `F12` - Open DevTools
- `Ctrl+Shift+I` - Open Inspector
- `Ctrl+Shift+J` - Open Console
- `Ctrl+Shift+Delete` - Clear Cache
- `Ctrl+Shift+N` - New Incognito Window

### Network Debugging
1. Open DevTools (F12)
2. Go to Network tab
3. Make request
4. See request/response details
5. Check Status codes (200 = OK, 404 = Not Found)

### Console Errors
1. Open Console (F12)
2. Look for red error messages
3. Click to see full error
4. Check line number
5. Fix in code

---

## 🔗 External Resources

- **Django Docs:** https://docs.djangoproject.com/
- **Ollama:** https://ollama.ai/
- **Python:** https://www.python.org/
- **SQLite:** https://www.sqlite.org/
- **JavaScript:** https://developer.mozilla.org/

---

## 🎓 Learning Resources

### Django Concepts
- Models: Object-relational mapping
- Views: Logic and data handling
- Templates: HTML rendering
- URLs: Request routing
- Forms: User input validation
- Admin: Data management interface

### Ollama Integration
- API calls via HTTP POST
- JSON request/response format
- Timeout handling
- Error management
- Model selection

### Database
- CRUD operations
- Foreign keys and relationships
- JSON fields
- Indexing for performance
- Query optimization

---

## 🆘 Getting Help

### When Something Breaks

1. **Check Error Message** - Read the error carefully
2. **Google the Error** - Common issues have solutions
3. **Check Terminal 3** - Django logs show what went wrong
4. **Run Verification** - `python test_setup.py`
5. **Reset Everything** - Follow Troubleshooting Checklist
6. **Ask for Help** - Share full error message

### Debug Strategy

1. **Isolate the Problem** - Which feature is broken?
2. **Check Basics** - Ollama running? Django running?
3. **View Logs** - Check Terminal 3 for errors
4. **Test Manually** - Use Django shell to test
5. **Search Online** - Copy error message to search

---

## 📈 Next Steps

### For Learners
- [ ] Follow STARTUP_GUIDE.md
- [ ] Test each feature
- [ ] Read DEVELOPMENT.md
- [ ] Modify templates
- [ ] Add new model
- [ ] Create new view

### For Developers
- [ ] Review PROJECT_SUMMARY.md
- [ ] Explore codebase
- [ ] Implement interview scoring
- [ ] Add PDF export
- [ ] Integrate real ML model
- [ ] Deploy to production

### For Improvements
- [ ] Add user authentication
- [ ] Implement pagination
- [ ] Add data visualization
- [ ] Create API documentation
- [ ] Write unit tests
- [ ] Set up CI/CD

---

## 📋 Version Info

- **Python:** 3.9+
- **Django:** 5.2.8
- **Ollama:** Latest
- **Model:** Mistral 7B
- **Database:** SQLite
- **OS:** Windows (PowerShell)

---

## ✅ Final Checklist

Before using in production:
- [ ] Run `python test_setup.py` - All green ✅
- [ ] Test all 5 features
- [ ] Create admin user
- [ ] Backup database
- [ ] Test Ollama integration
- [ ] Review security settings
- [ ] Configure ALLOWED_HOSTS
- [ ] Set DEBUG = False (for production)
- [ ] Set up error logging
- [ ] Configure HTTPS
- [ ] Setup database backups
- [ ] Document deployment steps

---

**Career Compass** - Quick Reference v1.0  
**Last Updated:** 2024  
**Status:** Ready to Use ✅
