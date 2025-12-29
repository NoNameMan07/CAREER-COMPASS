# 📖 Career Compass Development Documentation

## Architecture Overview

Career Compass is a Django-based AI platform with Ollama integration. It follows the Model-View-Template (MVT) pattern.

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP
       ▼
┌──────────────────┐
│  Django Views    │ ◄── renders templates
└────────┬─────────┘
         │
         ├─► Database (SQLite)
         ├─► Ollama API (localhost:11434)
         └─► File System
```

---

## Project Structure

```
CAREER/
├── manage.py                 # Django CLI
├── db.sqlite3               # SQLite Database
├── requirements.txt         # Dependencies
│
├── myproject/               # Django Project Config
│   ├── __init__.py
│   ├── settings.py          # All settings
│   ├── urls.py              # Root URL routing
│   ├── asgi.py              # ASGI for deployment
│   └── wsgi.py              # WSGI for deployment
│
├── main/                    # Main Application
│   ├── __init__.py
│   ├── models.py            # 7 Database models
│   ├── views.py             # Views & API endpoints
│   ├── forms.py             # Django forms
│   ├── urls.py              # URL patterns
│   ├── admin.py             # Admin interface
│   ├── apps.py
│   ├── tests.py
│   └── migrations/          # DB migrations
│       ├── 0001_initial.py
│       ├── 0002_...py
│       └── __init__.py
│
├── templates/
│   └── main/
│       ├── base.html        # Master template
│       ├── index.html       # Home/Dashboard
│       ├── chat.html        # Chat interface
│       ├── recommendations.html
│       ├── interview.html
│       ├── resume.html
│       └── cover_letter.html
│
├── static/
│   └── css/
│       └── style.css
│
└── docs/
    ├── STARTUP_GUIDE.md     # Quick start
    ├── DEVELOPMENT.md       # This file
    └── API_REFERENCE.md     # API docs
```

---

## Database Models

### 1. Profile
```python
class Profile(models.Model):
    name = CharField(max_length=100)
    email = EmailField()
    location = CharField(max_length=100, blank=True)
    created_at = DateTimeField(auto_now_add=True)
```
**Purpose:** Store user profile information
**Relations:** One-to-many with Recommendation

### 2. Conversation
```python
class Conversation(models.Model):
    title = CharField(max_length=200)
    created_at = DateTimeField(auto_now_add=True)
```
**Purpose:** Group chat messages into conversations
**Relations:** One-to-many with Message

### 3. Message
```python
class Message(models.Model):
    conversation = ForeignKey(Conversation)
    role = CharField(choices=[('user', 'User'), ('assistant', 'Assistant')])
    text = TextField()
    created_at = DateTimeField(auto_now_add=True)
```
**Purpose:** Individual messages in conversations
**Relations:** Foreign key to Conversation

### 4. Recommendation
```python
class Recommendation(models.Model):
    profile = ForeignKey(Profile)
    recommended_roles = TextField()  # CSV string
    created_at = DateTimeField(auto_now_add=True)
```
**Purpose:** Store career recommendations
**Relations:** Foreign key to Profile

### 5. InterviewAttempt
```python
class InterviewAttempt(models.Model):
    role = CharField(max_length=100)
    questions = JSONField()  # Array of questions
    answers = JSONField()    # Array of answers
    score = IntegerField()
    created_at = DateTimeField(auto_now_add=True)
```
**Purpose:** Store mock interview attempts
**Storage:** Questions and answers in JSON format

### 6. Resume
```python
class Resume(models.Model):
    name = CharField(max_length=100)
    data_json = JSONField()  # Complete resume data
    created_at = DateTimeField(auto_now_add=True)
```
**Purpose:** Store resume data
**Storage:** All resume sections in JSON

### 7. CoverLetter
```python
class CoverLetter(models.Model):
    name = CharField(max_length=100)
    role = CharField(max_length=100)
    body = TextField()
    created_at = DateTimeField(auto_now_add=True)
```
**Purpose:** Store generated cover letters

---

## Views & URL Routing

### Main Views

| View | URL | Method | Purpose |
|------|-----|--------|---------|
| `index` | `/` | GET | Homepage with statistics |
| `chat_page` | `/chat/` | GET | Chat interface |
| `chat_api` | `/api/chat/` | POST | Chat API endpoint |
| `recommendations_page` | `/recommendations/` | GET | Recommendations form |
| `recommend_api` | `/api/recommend/` | POST | Recommendations API |
| `interview_page` | `/interview/` | GET | Interview interface |
| `interview_api` | `/api/interview/` | POST | Interview API |
| `resume_page` | `/resume/` | GET | Resume form |
| `resume_download` | `/resume/download/` | POST | Resume download |
| `cover_letter_page` | `/cover-letter/` | GET | Cover letter form |
| `cover_letter_api` | `/api/cover-letter/` | POST | Cover letter API |

### URL Patterns (main/urls.py)
```python
urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_page, name='chat_page'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('recommendations/', views.recommendations_page, name='recommendations_page'),
    path('api/recommend/', views.recommend_api, name='recommend_api'),
    path('interview/', views.interview_page, name='interview_page'),
    path('api/interview/', views.interview_api, name='interview_api'),
    path('resume/', views.resume_page, name='resume_page'),
    path('resume/download/', views.resume_download, name='resume_download'),
    path('cover-letter/', views.cover_letter_page, name='cover_letter_page'),
    path('api/cover-letter/', views.cover_letter_api, name='cover_letter_api'),
]
```

---

## Ollama Integration

### call_ollama() Function
```python
def call_ollama(prompt: str, system_prompt: str = "") -> str:
    """
    Calls Ollama API and returns generated text.
    
    Args:
        prompt (str): User's input prompt
        system_prompt (str): System context/instructions
    
    Returns:
        str: Generated response from Ollama
    """
    try:
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        response = requests.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=30
        )
        return response.json().get("response", "No response")
    except requests.exceptions.ConnectionError:
        return "Error: Ollama not running"
```

### Configuration
```python
# In views.py
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"
```

### Career Roles
```python
VALID_CAREER_ROLES = [
    "Data Scientist", "Machine Learning Engineer", 
    "Software Developer", "Cloud Architect", "DevOps Engineer",
    "Product Manager", "UX Designer", "Data Engineer",
    "Business Analyst", "Solutions Architect", "Security Engineer",
    "QA Engineer", "Technical Lead", "Frontend Developer",
    "Backend Developer", "Full Stack Developer", "Database Administrator",
    "Systems Administrator", "IT Support Specialist", "Technical Writer"
]
```

---

## API Endpoints

### 1. Chat API
**Endpoint:** `POST /api/chat/`

**Request:**
```json
{
  "text": "What skills do I need for a Data Science role?"
}
```

**Response:**
```json
{
  "response": "To become a Data Scientist...",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Logic:**
1. Receives user message
2. Creates/updates Conversation (from session)
3. Creates Message (user role)
4. Calls `call_ollama()` with chat context
5. Saves response Message (assistant role)
6. Returns JSON response

### 2. Recommendations API
**Endpoint:** `POST /api/recommend/`

**Request:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "education": "Bachelor's",
  "experience": 5,
  "skills": "Python, SQL, Machine Learning",
  "selected_roles": ["Data Scientist", "ML Engineer"]
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "role": "Data Scientist",
      "match_score": 85,
      "trend": "📈 Rising"
    },
    {
      "role": "ML Engineer",
      "match_score": 78,
      "trend": "📈 Rising"
    }
  ]
}
```

**Logic:**
1. Creates Profile with user data
2. Performs skill-to-role matching
3. Filters by selected roles (if provided)
4. Adds market trend data
5. Creates Recommendation record
6. Returns JSON

### 3. Interview API
**Endpoint:** `POST /api/interview/`

**Request:**
```json
{
  "role": "Data Scientist",
  "questions_count": 10
}
```

**Response:**
```json
{
  "questions": [
    "Explain the difference between supervised and unsupervised learning",
    "How would you handle missing data in a dataset?",
    // ... more questions
  ],
  "attempt_id": 123,
  "role": "Data Scientist"
}
```

**Logic:**
1. Validates role against VALID_CAREER_ROLES
2. Creates system prompt for Ollama
3. Generates questions via Ollama
4. Parses response into array
5. Creates InterviewAttempt record
6. Returns questions array

### 4. Cover Letter API
**Endpoint:** `POST /api/cover-letter/`

**Request:**
```json
{
  "name": "Jane Smith",
  "role": "Senior Software Engineer",
  "company": "Tech Corp Inc",
  "context": "Looking to transition from frontend to backend"
}
```

**Response:**
```json
{
  "cover_letter": "Dear Hiring Manager,\n\nI am writing..."
}
```

**Logic:**
1. Builds prompt from user data
2. Calls Ollama with system prompt
3. Saves to CoverLetter model
4. Returns generated letter

### 5. Resume API
**Endpoint:** `POST /resume/download/`

**Request:** Form submission with:
- Name, Summary
- Work Experience
- Education
- Skills, Certifications

**Response:** JSON file download

**Logic:**
1. Validates form data
2. Converts to JSON
3. Saves to Resume model
4. Returns JSON file for download

---

## Forms

### ProfileForm
```python
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'})
        }
```

### ResumeForm
Custom form with fields:
- name (CharField)
- summary (CharField)
- experiences (CharField)
- education (CharField)
- skills (CharField)
- certifications (CharField)

### CoverLetterForm
Fields:
- name (CharField)
- role (CharField)
- company (CharField)
- context (CharField)

---

## Templates

### base.html
Master template with:
- Gradient navbar (purple gradient)
- Navigation links
- CSS styling (inline)
- Block for child content
- Alert/message handling

### index.html
Homepage with:
- Statistics dashboard (4 metrics)
- Feature cards (5 features)
- Getting started guide
- Links to all features

### chat.html
Chat interface with:
- Messages display area
- Input form
- Sidebar with conversation history
- JavaScript for AJAX calls
- Auto-scroll functionality

### recommendations.html
Form with:
- Name, email fields
- Education dropdown
- Experience input
- Skills textarea
- Role selection buttons
- Results display

### interview.html
Interview interface with:
- Role dropdown
- Question count selector
- Questions display
- Answer textareas
- Submit button
- Results/feedback area

### resume.html
Form with:
- Personal information section
- Professional background section
- Skills & certifications section
- Submit button

### cover_letter.html
Form with:
- Name, role fields
- Company, context fields
- Submit button
- Results display with copy button

---

## Frontend JavaScript

### Chat Submission (chat.html)
```javascript
document.getElementById('chat-form').addEventListener('submit', async function(e){
    e.preventDefault();
    const text = document.getElementById('text').value.trim();
    
    // Display user message
    const userDiv = document.createElement('div');
    userDiv.textContent = text;
    messagesDiv.appendChild(userDiv);
    
    // Call API
    const response = await fetch('{% url "chat_api" %}', {
        method: 'POST',
        body: JSON.stringify({text}),
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': csrftoken}
    });
    
    const data = await response.json();
    
    // Display AI response
    const aiDiv = document.createElement('div');
    aiDiv.textContent = data.response;
    messagesDiv.appendChild(aiDiv);
    
    scrollToBottom();
    document.getElementById('chat-form').reset();
});
```

### CSRF Token Retrieval
```javascript
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
```

---

## Adding New Features

### Step 1: Create Model
Edit `main/models.py`:
```python
class MyModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.field1
```

### Step 2: Create Migration
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Register in Admin
Edit `main/admin.py`:
```python
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'created_at')
    search_fields = ('field1',)
    list_filter = ('created_at',)

admin.site.register(MyModel, MyModelAdmin)
```

### Step 4: Create View
Edit `main/views.py`:
```python
def my_feature_page(request):
    data = MyModel.objects.all()
    return render(request, 'main/my_feature.html', {'data': data})

@csrf_exempt
def my_feature_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Process data
        result = call_ollama(f"Prompt: {data['input']}")
        return JsonResponse({'result': result})
```

### Step 5: Create URL
Edit `main/urls.py`:
```python
path('my-feature/', views.my_feature_page, name='my_feature_page'),
path('api/my-feature/', views.my_feature_api, name='my_feature_api'),
```

### Step 6: Create Template
Create `templates/main/my_feature.html`:
```html
{% extends 'main/base.html' %}
{% block title %}My Feature{% endblock %}
{% block content %}
<h2>My Feature</h2>
<form id="my-form">
    {% csrf_token %}
    <input type="text" id="input" placeholder="Enter something">
    <button type="submit">Submit</button>
</form>
<div id="result"></div>

<script>
document.getElementById('my-form').addEventListener('submit', async function(e){
    e.preventDefault();
    const input = document.getElementById('input').value;
    const response = await fetch('{% url "my_feature_api" %}', {
        method: 'POST',
        body: JSON.stringify({input}),
        headers: {'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken')}
    });
    const data = await response.json();
    document.getElementById('result').textContent = data.result;
});
</script>
{% endblock %}
```

---

## Debugging

### Django Debug Mode
In `myproject/settings.py`:
```python
DEBUG = True  # Set to False in production
```

### Check Syntax Errors
```powershell
python manage.py check
```

### Database Inspection
```powershell
python manage.py dbshell
# View tables: .tables
# Query data: SELECT * FROM main_profile;
```

### Django Shell
```powershell
python manage.py shell
>>> from main.models import Profile
>>> Profile.objects.all()
>>> Profile.objects.create(name="Test", email="test@test.com")
```

### View Logs
Check Terminal 3 (Django server terminal) for:
- Request logs
- Error messages
- SQL queries (if DEBUG=True)

### Browser Console
Press `F12` in browser to view:
- JavaScript errors
- Network requests
- Console logs

---

## Performance Optimization

### Database Queries
Use `.select_related()` and `.prefetch_related()`:
```python
# Good
conversations = Conversation.objects.prefetch_related('message_set')

# Bad (N+1 problem)
for conv in Conversation.objects.all():
    print(conv.message_set.all())
```

### Ollama Response Time
- First call: 10-30 seconds (model loading)
- Subsequent: 2-5 seconds
- Consider async tasks for production

### Database Indexing
```python
class MyModel(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
```

---

## Deployment Checklist

Before deploying to production:

- [ ] Set `DEBUG = False`
- [ ] Set `ALLOWED_HOSTS` properly
- [ ] Use environment variables for secrets
- [ ] Run `python manage.py collectstatic`
- [ ] Set up production database (PostgreSQL)
- [ ] Configure Ollama for production (consider API server)
- [ ] Set up error logging (Sentry)
- [ ] Enable HTTPS
- [ ] Configure CSRF and CORS properly
- [ ] Set up automated backups
- [ ] Use gunicorn/uWSGI instead of runserver

---

## Testing

### Create Test File
Create `main/tests.py`:
```python
from django.test import TestCase, Client
from main.models import Profile
from main.views import call_ollama

class ProfileTests(TestCase):
    def setUp(self):
        self.profile = Profile.objects.create(
            name="Test User",
            email="test@example.com"
        )
    
    def test_profile_creation(self):
        self.assertEqual(self.profile.name, "Test User")
    
    def test_chat_view(self):
        client = Client()
        response = client.get('/chat/')
        self.assertEqual(response.status_code, 200)
```

### Run Tests
```powershell
python manage.py test
python manage.py test main.tests.ProfileTests
python manage.py test --keepdb  # Don't recreate DB
```

---

## Resources

- Django Documentation: https://docs.djangoproject.com/
- Ollama API: https://github.com/ollama/ollama/blob/main/docs/api.md
- ReportLab PDF: https://www.reportlab.com/docs/reportlab-userguide.pdf
- SQLite: https://www.sqlite.org/

---

## Troubleshooting Development Issues

### Migrations Won't Apply
```powershell
python manage.py migrate main zero  # Rollback
python manage.py migrate main       # Reapply
```

### Static Files Not Loading
```powershell
python manage.py collectstatic --noinput
```

### Models Conflict
```powershell
python manage.py makemigrations --merge
```

### Import Errors
```powershell
# Ensure main app is in INSTALLED_APPS
# Check settings.py for typos
# Verify __init__.py files exist
```

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Author:** Career Compass Development Team
