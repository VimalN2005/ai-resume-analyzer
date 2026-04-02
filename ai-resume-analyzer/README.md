# 🔍 AI-Powered Resume Analyzer

> Full-stack Django web app that analyzes resumes against job descriptions using spaCy NLP, delivering instant **ATS score**, keyword gap analysis, and job-role match percentage.

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)
![spaCy](https://img.shields.io/badge/spaCy-3.6-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---

## 📌 Features
- 📄 Upload PDF resume → instant analysis
- 🎯 ATS Score (0–100) using cosine similarity
- 🔑 Keyword Gap Analysis — missing vs matched skills
- 💼 Job-role match percentage
- 🔐 User authentication & session management
- 📊 Analysis history dashboard
- 📱 Responsive Bootstrap 5 UI

---

## 📁 Project Structure
```
ai-resume-analyzer/
├── resume_analyzer/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── analyzer/
│   ├── models.py           # Django ORM models
│   ├── views.py            # Request handlers
│   ├── urls.py             # URL routing
│   ├── nlp_pipeline.py     # spaCy NLP + ATS scoring
│   ├── forms.py            # Upload & auth forms
│   └── templates/
│       ├── base.html
│       ├── upload.html
│       ├── results.html
│       ├── history.html
│       ├── login.html
│       └── register.html
├── media/resumes/          # Uploaded PDFs (gitignored)
├── manage.py
├── requirements.txt
└── README.md
```

---

## 🚀 Setup & Run

### 1. Clone & Create Virtual Environment
```bash
git clone https://github.com/VimalN2005/ai-resume-analyzer.git
cd ai-resume-analyzer
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_md
```

### 3. Apply Migrations
```bash
python manage.py migrate
python manage.py createsuperuser   # optional admin access
```

### 4. Run the Server
```bash
python manage.py runserver
# Open: http://127.0.0.1:8000
```

---

## 📦 Requirements
```
django==4.2.7
spacy==3.6.1
pymupdf==1.23.3
scikit-learn==1.3.0
numpy==1.24.3
python-dotenv==1.0.0
Pillow==10.0.0
```

## 👤 Author
**Vimal Sahani** — IIIT Bhopal | [GitHub](https://github.com/VimalN2005) | [LinkedIn](https://linkedin.com/in/n-vimal-60b624379)
