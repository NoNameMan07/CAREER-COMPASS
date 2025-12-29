# 🎯 Career Compass - AI-Powered Career Guidance

A Django-based web application that provides AI-powered career guidance with features for chatting with an AI advisor, getting career recommendations, practicing interviews, building resumes, and generating cover letters.

## 🌟 Features

✅ **AI Chat** - Have conversations with an AI career advisor
✅ **Career Recommendations** - Get personalized career suggestions based on your skills
✅ **Mock Interview** - Practice interview questions for target roles
✅ **Resume Builder** - Create professional resumes and download as data
✅ **Cover Letter Generator** - Generate personalized cover letters

## 🛠️ Tech Stack

- **Framework**: Django 5.2.8
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Database**: SQLite (built-in)
- **PDF Generation**: ReportLab

## 📋 Installation & Setup (Windows PowerShell)

### Step 1: Create Virtual Environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Create Superuser (Admin Access)
```powershell
python manage.py createsuperuser
# Follow the prompts to create username, email, password
```

### Step 5: Start Development Server
```powershell
python manage.py runserver
```

The application will be available at: **http://127.0.0.1:8000**

## 🚀 Usage

### Home Page
Visit http://127.0.0.1:8000/ to see all available features with quick-access buttons.

### Chat Feature (💬)
1. Go to http://127.0.0.1:8000/chat/
2. Type your question or career concern
3. Get responses from the AI advisor
4. Chat history is stored in the database

### Career Recommendations (🔮)
1. Go to http://127.0.0.1:8000/recommendations/
2. Enter your name and skills (comma-separated)
3. Receive personalized career recommendations
4. Results are saved to your profile

### Mock Interview (🎯)
1. Go to http://127.0.0.1:8000/interview/
2. Select your target role
3. Choose number of questions (5, 10, or 15)
4. Get interview questions to practice
5. Results are stored for later review

### Resume Builder (📝)
1. Go to http://127.0.0.1:8000/resume/
2. Fill in your information:
   - Professional summary
   - Work experience
   - Education
   - Skills
3. Submit to save and download
4. Resume data is stored in database

### Cover Letter Generator (📄)
1. Go to http://127.0.0.1:8000/cover-letter/
2. Enter your name, target role, and context
3. Get a generated cover letter
4. Copy to clipboard for use

## 🔐 Admin Panel

Access the Django admin at: **http://127.0.0.1:8000/admin/**

Log in with your superuser credentials to:
- View/manage conversations and messages
- View career recommendations
- View interview attempts
- View saved resumes and cover letters
- View user profiles

## 📁 Project Structure

```
CAREER/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── db.sqlite3                # SQLite database
├── myproject/                # Django project config
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py              # ASGI config
│   └── wsgi.py              # WSGI config
├── main/                     # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL routing
│   ├── admin.py             # Admin configuration
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   └── main/
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       ├── chat.html        # Chat page
│       ├── recommendations.html
│       ├── interview.html
│       ├── resume.html
│       └── cover_letter.html
└── static/                  # Static files
    └── css/
        └── style.css        # Styles
```

## 🛠️ Common Commands

```powershell
# Activate virtual environment
.venv\Scripts\Activate.ps1

# Create migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Start development server
python manage.py runserver

# Create superuser for admin
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic
```

## 📊 Database Models

### Profile
- name, email, location
- Tracks user information

### Conversation
- title, created_at
- Stores chat sessions

### Message
- conversation (FK), role, text, created_at
- Individual messages in conversations

### Recommendation
- profile (FK), recommended_roles, created_at
- Career recommendations for users

### InterviewAttempt
- role, questions, answers, score, created_at
- Interview practice sessions

### Resume
- name, data_json, created_at
- Saved resume information

### CoverLetter
- name, role, body, created_at
- Generated cover letters

## 🔄 Future Enhancements

- Integration with real AI models (Ollama, GPT)
- PDF download for resumes and cover letters
- User authentication and accounts
- Email integration for cover letters
- Job board API integration
- Advanced analytics and progress tracking
- Mobile app version

## 📝 License

This project is provided as-is for educational and personal use.

## 👤 Support

For questions or issues, please refer to the documentation or create an issue in the repository.

---

**Made with ❤️ for career guidance**
