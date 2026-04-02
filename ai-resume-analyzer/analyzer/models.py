"""
models.py — Database Models
AI Resume Analyzer | Vimal Sahani
"""

from django.db import models
from django.contrib.auth.models import User


def resume_upload_path(instance, filename):
    return f"resumes/{instance.user.username}/{filename}"


class ResumeAnalysis(models.Model):
    """Stores each resume analysis result for a user."""

    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name="analyses")
    resume_file    = models.FileField(upload_to=resume_upload_path)
    job_role       = models.CharField(max_length=200)
    job_description= models.TextField()

    # ── NLP Results ──────────────────────────────────────
    ats_score         = models.FloatField(default=0.0)      # 0–100
    match_percentage  = models.FloatField(default=0.0)      # 0–100
    matched_keywords  = models.JSONField(default=list)
    missing_keywords  = models.JSONField(default=list)
    resume_text       = models.TextField(blank=True)
    word_count        = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Resume Analyses"

    def __str__(self):
        return f"{self.user.username} | {self.job_role} | ATS: {self.ats_score:.1f}"

    @property
    def ats_grade(self):
        if self.ats_score >= 80: return ("Excellent", "success")
        if self.ats_score >= 60: return ("Good",      "primary")
        if self.ats_score >= 40: return ("Average",   "warning")
        return ("Needs Work", "danger")
