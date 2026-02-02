# 🎯 Career Compass Sensei - AI-Powered Career Guidance & Emotional Support System

An intelligent Django-based web application that provides AI-powered career guidance with personalized recommendations, emotional intelligence, mock interviews, professional resume building, and AI-driven career counseling. Built using Design Thinking methodology with NLP, Machine Learning, and sentiment analysis.

**Repository**: [GitHub - Career Compass](https://github.com/NoNameMan07/CAREER-COMPASS.git)

---

## 🌟 Features

✅ **AI Chat Advisor** - Conversational AI career guidance with sentiment analysis and emotional intelligence
✅ **Smart Career Recommendations** - ML-powered top-5 role predictions from user skills (using TF-IDF + Logistic Regression)
✅ **Real-Time Market Trends** - Live job market data from U.S. Bureau of Labor Statistics (BLS)
✅ **Mock Interview Practice** - MCQ flashcard-style interviews with AI-generated questions for target roles
✅ **Professional Resume Builder** - Two-column reference-style resume with client-side PDF export
✅ **Cover Letter Generator** - AI-powered personalized cover letters
✅ **Skill Gap Analysis** - Identifies missing skills for target roles with learning roadmap
✅ **Interactive Dashboard** - Career demand visualization with 5-year job market graphs
✅ **Sentiment Analysis** - Emotion-aware responses tailored to user emotional state

---

## 🛠️ Tech Stack

**Backend:**
- Django 5.2.8
- Python 3.10+
- SQLite / PostgreSQL

**Frontend:**
- HTML5 + CSS3
- Vanilla JavaScript
- html2pdf.js for client-side PDF generation

**Machine Learning & AI:**
- Scikit-learn (TF-IDF Vectorizer, Logistic Regression)
- XGBoost (alternative ensemble model)
- Mistral 7B via Ollama (LLM for chat & MCQ generation)
- VADER Sentiment Analysis

**Data & APIs:**
- U.S. Bureau of Labor Statistics (BLS) - Real job market data
- Synthetic Career Dataset (2,500 samples, 20 roles)

**Additional:**
- Joblib for model persistence
- Pandas + NumPy for data processing
- ReportLab for PDF generation

---

## 📋 Complete Setup Guide for New Device

### **Prerequisites**

Before starting, ensure you have installed:
- **Python 3.10 or higher** ([Download](https://www.python.org/))
- **Git** ([Download](https://git-scm.com/))
- **Ollama** (Optional, for local LLM) ([Download](https://ollama.ai/))
- **pip** (comes with Python)

#### Verify installations:
```powershell
python --version
git --version
pip --version
```

---

### **Step 1: Clone the Repository**

```powershell
cd Desktop
git clone https://github.com/NoNameMan07/CAREER-COMPASS.git
cd CAREER-COMPASS
```

---

### **Step 2: Create & Activate Virtual Environment**

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux (Bash):**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

### **Step 3: Upgrade pip & Install Dependencies**

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**Key packages installed:**
- Django 5.2.8
- scikit-learn (ML models)
- pandas, numpy (data processing)
- joblib (model persistence)
- requests (API calls)
- reportlab (PDF generation)

---

### **Step 4: Database Setup**

```powershell
python manage.py makemigrations
python manage.py migrate
```

This creates the SQLite database and applies all migrations.

---

### **Step 5: Create Django Superuser (Admin Access)**

```powershell
python manage.py createsuperuser
```

Follow prompts:
```
Username: admin
Email: admin@example.com
Password: (choose a secure password)
```

---

### **Step 6: Verify ML Model Setup**

The pre-trained role matcher model should exist at `models/role_matcher.joblib`:
```powershell
ls models/  # Verify role_matcher.joblib exists
```

If missing, regenerate it:
```powershell
python scripts/train_role_model.py
```

This trains the ML model on the synthetic career dataset.

---

### **Step 7: (Optional) Setup Local Ollama LLM**

For AI chat and interview MCQ generation without external API calls:

1. Install Ollama: https://ollama.ai/
2. Start Ollama service:
```powershell
ollama serve
```

3. In another terminal, pull Mistral model:
```powershell
ollama pull mistral
```

4. Verify in Django settings (`myproject/settings.py`):
```python
OLLAMA_URL = "http://localhost:11434"
OLLAMA_MODEL = "mistral"
```

---

### **Step 8: Start Development Server**

```powershell
python manage.py runserver
```

Output:
```
Starting development server at http://127.0.0.1:8000/
```

---

### **Step 9: Access the Application**

Open your browser and navigate to:

| Page | URL |
|------|-----|
| **Home** | http://127.0.0.1:8000/ |
| **Career Recommendations** | http://127.0.0.1:8000/recommendations/ |
| **Mock Interview** | http://127.0.0.1:8000/interview/ |
| **Resume Builder** | http://127.0.0.1:8000/resume/ |
| **Cover Letter** | http://127.0.0.1:8000/cover-letter/ |
| **Chat** | http://127.0.0.1:8000/chat/ |
| **Admin Panel** | http://127.0.0.1:8000/admin/ |

---

## 🎯 Using the Application

### **1. Career Recommendations**
- Select 3-8 skills from the comprehensive skill grid (105+ skills)
- Choose risk level, work preference, sentiment
- View top-5 recommended roles with:
  - Match percentage
  - Skill gaps analysis
  - 5-year job market growth graphs (real BLS data)
  - Learning roadmap for the top role

### **2. Mock Interview**
- Select target role and number of questions
- AI generates MCQ flashcard-style questions
- 30-second timer per question
- Instant scoring with review
- Session ID saved for history

### **3. Resume Builder**
- Fill in personal info, professional summary
- Parse work experience (use "---" to separate entries)
- Parse education entries
- Add skills and certifications
- Click "Client-side PDF" to export as styled resume PDF

### **4. AI Chat**
- Ask career-related questions
- Get emotionally intelligent responses
- Sentiment analysis on messages
- Conversation history saved

---

## 📊 Project Structure

```
CAREER-COMPASS/
├── main/                          # Django app
│   ├── views.py                   # API endpoints & business logic
│   ├── models.py                  # Database models
│   ├── forms.py                   # Django forms
│   ├── urls.py                    # URL routing
│   └── utils/
│       └── sentiment.py           # Sentiment analysis
├── templates/
│   └── main/
│       ├── recommendations_new.html   # Career recommendations UI
│       ├── interview.html            # Mock interview UI
│       ├── resume.html               # Resume builder UI
│       ├── chat.html                 # AI chat UI
│       └── ...
├── static/
│   └── css/style.css              # Stylesheet
├── data/
│   ├── synthetic_career_data.csv  # Training data (2,500 rows, 20 roles)
│   └── generate_synthetic.py      # Synthetic data generator
├── models/
│   └── role_matcher.joblib        # Trained ML model (TF-IDF + LogReg)
├── scripts/
│   └── train_role_model.py        # Model training script
├── notebooks/
│   └── role_model_training.ipynb  # Jupyter notebook for model training
├── src/
│   ├── configs/
│   │   ├── role_required_skills.json
│   │   └── skill_to_course.json
│   ├── artifacts/
│   │   └── (XGBoost models, encoders, metrics)
│   └── ...
├── myproject/
│   ├── settings.py                # Django configuration
│   ├── urls.py                    # Project-level URL config
│   └── wsgi.py
├── manage.py                      # Django CLI
├── requirements.txt               # Python dependencies
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

---

## 🤖 ML Model Details

### **Role Matcher Pipeline** (`models/role_matcher.joblib`)

**Components:**
1. **TF-IDF Vectorizer** - Converts skill text to numerical features
2. **Logistic Regression** - Multiclass classifier (20 roles)
3. **Label Encoder** - Maps role names ↔ numeric labels

**Training Data:**
- 2,500 synthetic resumes
- 105+ technical & soft skills
- 20 career roles
- 80/20 train/validation split

**Metrics:**
- Top-1 Accuracy: 49.4%
- Top-5 Accuracy: 90.2%

**How it works:**
```
User Skills (string)
    ↓
TF-IDF Vectorization
    ↓
Logistic Regression (probability per role)
    ↓
Top-5 roles ranked by score
```

**Regenerate model:**
```powershell
python scripts/train_role_model.py
```

---

## 🔌 API Endpoints

### **Career Recommendations**
```
POST /api/recommend/
{
  "name": "John Doe",
  "skills": ["python", "sql", "django"],
  "education": "Bachelors",
  "experience": 2,
  "risk_taking": "medium",
  "work_preference": "team",
  "sentiment": "neutral",
  "motivation_score": 70,
  "interests": {"data": 4, "programming": 5, "design": 2, "management": 2}
}

Response:
{
  "recommendations": [
    {"role": "Backend Developer", "score": 0.85},
    {"role": "Software Developer", "score": 0.78},
    ...
  ],
  "skill_gap": {"required": [], "have": [], "missing": []},
  "learning_plan": [...],
  "market_trend": {...},
  "market_trend_values": {...}
}
```

### **Interview Generation**
```
POST /interview_api/
{
  "role": "Backend Developer",
  "count": 5
}

Response:
{
  "mcqs": [
    {
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer_index": 0
    }
  ],
  "attempt_id": 1,
  "role": "Backend Developer",
  "generation_ms": 2345
}
```

### **Chat**
```
POST /chat_api/
{
  "text": "How do I become a data scientist?"
}

Response:
{
  "response": "AI response here...",
  "conversation_id": 5
}
```

---

## 📈 Real-Time Data Integration

### **Bureau of Labor Statistics (BLS) Data**

Real job market statistics integrated in `main/views.py`:
- **Software Developer**: 129,200 annual openings, 1.9M jobs, 15% growth
- **Cybersecurity Analyst**: 16,000 annual openings, 182.8K jobs, 29% growth
- **Data Scientist**: 22,000 annual openings, 220K jobs, 34% growth
- **And 17 more roles...**

Source: [BLS Occupational Outlook Handbook](https://www.bls.gov/ooh/)

---

## 🧠 Sentiment Analysis

Uses VADER (Valence Aware Dictionary and sEntiment Reasoner):
- Analyzes user messages for emotion
- Triggers emotion-aware responses
- Adjusts chatbot tone based on sentiment
- Stored in conversation history

---

## 🚨 Troubleshooting

### **Issue: Virtual environment not activating**
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

### **Issue: "ModuleNotFoundError: No module named 'django'"**
**Solution:**
```powershell
pip install -r requirements.txt
```

### **Issue: "Port 8000 is already in use"**
**Solution:**
```powershell
python manage.py runserver 8001  # Use different port
```

### **Issue: Model not found (role_matcher.joblib missing)**
**Solution:**
```powershell
python scripts/train_role_model.py
```

### **Issue: Ollama connection error**
**Solution:**
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_URL` in `myproject/settings.py` is correct
- Fallback: System uses heuristic scoring without Ollama

### **Issue: Database errors**
**Solution:**
```powershell
python manage.py migrate --run-syncdb
python manage.py makemigrations
python manage.py migrate
```

---

## 📚 Learning Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Scikit-learn**: https://scikit-learn.org/
- **BLS Data**: https://www.bls.gov/ooh/
- **Design Thinking**: https://www.interaction-design.org/

---

## 🔒 Security Notes

- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Use PostgreSQL instead of SQLite for production
- Enable HTTPS
- Set allowed hosts
- Use environment variables for sensitive data

---

## 📝 License

This project is for educational purposes.

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Open pull request

---

## 📧 Support

For issues or questions, open an issue on GitHub or contact the development team.

---

**Last Updated**: February 2, 2026
**Version**: 1.0.0

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
