"""
nlp_pipeline.py — spaCy NLP Pipeline + ATS Scoring Engine
AI Resume Analyzer | Vimal Sahani

Pipeline:
  PDF → text extraction (PyMuPDF)
  → tokenization & NER (spaCy)
  → skill extraction
  → cosine similarity ATS scoring
"""

import re
import fitz          # PyMuPDF
import spacy
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


# ── Load spaCy model (medium — has word vectors) ───────────────────────────
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    raise OSError(
        "spaCy model not found. Run:\n"
        "  python -m spacy download en_core_web_md"
    )

# ── Comprehensive skill vocabulary ─────────────────────────────────────────
TECH_SKILLS = {
    # Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "sql",
    "go", "rust", "kotlin", "swift", "scala", "html", "css", "bash", "php",
    # ML / AI
    "machine learning", "deep learning", "neural network", "nlp",
    "natural language processing", "computer vision", "reinforcement learning",
    "transfer learning", "tensorflow", "keras", "pytorch", "scikit-learn",
    "xgboost", "lightgbm", "catboost", "opencv", "spacy", "nltk", "transformers",
    "bert", "gpt", "llm", "diffusion", "gan", "cnn", "rnn", "lstm", "attention",
    # Data
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "tableau", "power bi",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "data analysis", "data visualization", "feature engineering", "eda",
    # Web
    "django", "flask", "fastapi", "react", "node.js", "rest api", "graphql",
    "bootstrap", "html", "css", "javascript",
    # DevOps / Tools
    "git", "github", "docker", "kubernetes", "aws", "gcp", "azure",
    "linux", "jupyter", "vscode", "android studio", "ci/cd",
    # Concepts
    "agile", "object oriented", "microservices", "api", "system design",
    "data structures", "algorithms", "probability", "statistics",
}

SOFT_SKILLS = {
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "adaptability", "collaboration", "time management",
    "project management", "research", "analytical", "creative",
}

ALL_SKILLS = TECH_SKILLS | SOFT_SKILLS


# ── PDF Text Extraction ─────────────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract clean text from PDF using PyMuPDF."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")
    # Clean up whitespace
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ",    text)
    return text.strip()


# ── Skill Extraction ────────────────────────────────────────────────────────

def extract_skills(text: str) -> set:
    """Extract skills from text using vocabulary matching + NER."""
    text_lower = text.lower()
    found = set()

    # Direct vocabulary match
    for skill in ALL_SKILLS:
        if skill in text_lower:
            found.add(skill)

    # spaCy NER — catch proper nouns (e.g. "TensorFlow", "Django")
    doc = nlp(text[:100000])   # limit to avoid memory issues
    for ent in doc.ents:
        if ent.label_ in ("ORG", "PRODUCT", "GPE"):
            token = ent.text.lower().strip()
            if token in ALL_SKILLS:
                found.add(token)

    return found


def extract_named_entities(text: str) -> dict:
    """Extract named entities from resume (name, org, skills)."""
    doc = nlp(text[:50000])
    entities = {"PERSON": [], "ORG": [], "GPE": []}
    for ent in doc.ents:
        if ent.label_ in entities:
            entities[ent.label_].append(ent.text)
    return entities


# ── ATS Scoring ─────────────────────────────────────────────────────────────

def compute_cosine_ats_score(resume_text: str, jd_text: str) -> float:
    """
    Compute ATS score using TF-IDF cosine similarity.
    Returns score in range 0–100.
    """
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
        similarity   = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(similarity) * 100, 2)
    except Exception:
        return 0.0


def compute_spacy_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute semantic similarity using spaCy word vectors.
    Returns score in range 0–100.
    """
    doc1 = nlp(resume_text[:10000])
    doc2 = nlp(jd_text[:10000])
    if doc1.vector_norm == 0 or doc2.vector_norm == 0:
        return 0.0
    return round(doc1.similarity(doc2) * 100, 2)


def keyword_gap_analysis(resume_skills: set, jd_skills: set) -> dict:
    """
    Compare resume skills vs JD skills.
    Returns matched, missing, and match percentage.
    """
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    total   = len(jd_skills) if jd_skills else 1

    return {
        "matched":          sorted(matched),
        "missing":          sorted(missing),
        "match_percentage": round(len(matched) / total * 100, 2),
    }


# ── Main Pipeline ────────────────────────────────────────────────────────────

def analyze_resume(pdf_path: str, job_role: str, job_description: str) -> dict:
    """
    Full analysis pipeline.

    Returns:
        dict with ats_score, match_percentage, matched_keywords,
        missing_keywords, resume_text, word_count
    """
    # 1. Extract text
    resume_text = extract_text_from_pdf(pdf_path)
    word_count  = len(resume_text.split())

    # 2. Extract skills from both resume and JD
    resume_skills = extract_skills(resume_text)
    jd_skills     = extract_skills(job_description + " " + job_role)

    # 3. ATS Score — blend TF-IDF + spaCy
    tfidf_score  = compute_cosine_ats_score(resume_text, job_description)
    spacy_score  = compute_spacy_similarity(resume_text, job_description)
    ats_score    = round(0.6 * tfidf_score + 0.4 * spacy_score, 2)

    # 4. Keyword gap analysis
    gap = keyword_gap_analysis(resume_skills, jd_skills)

    return {
        "ats_score":         min(ats_score, 100.0),
        "match_percentage":  gap["match_percentage"],
        "matched_keywords":  gap["matched"],
        "missing_keywords":  gap["missing"],
        "resume_text":       resume_text,
        "word_count":        word_count,
    }
