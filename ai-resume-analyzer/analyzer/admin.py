from django.contrib import admin
from .models import ResumeAnalysis


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display  = ("user", "job_role", "ats_score", "match_percentage", "word_count", "created_at")
    list_filter   = ("created_at",)
    search_fields = ("user__username", "job_role")
    readonly_fields = ("resume_text", "matched_keywords", "missing_keywords")
