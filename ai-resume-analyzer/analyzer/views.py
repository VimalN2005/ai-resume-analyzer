"""
views.py — Request Handlers
AI Resume Analyzer | Vimal Sahani
"""

import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import ResumeAnalysis
from .forms import ResumeUploadForm, CustomRegisterForm, CustomLoginForm
from .nlp_pipeline import analyze_resume


# ── Auth Views ──────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = CustomRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Welcome, {user.username}! 🎉")
        return redirect("home")
    return render(request, "analyzer/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Welcome back, {user.username}!")
        return redirect(request.GET.get("next", "home"))
    return render(request, "analyzer/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")


# ── Core App Views ───────────────────────────────────────────────────────────

@login_required
def home_view(request):
    """Landing page — shows upload form."""
    form = ResumeUploadForm()
    return render(request, "analyzer/upload.html", {"form": form})


@login_required
def analyze_view(request):
    """Handle resume upload + run NLP pipeline."""
    if request.method != "POST":
        return redirect("home")

    form = ResumeUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        messages.error(request, "Please fix the errors below.")
        return render(request, "analyzer/upload.html", {"form": form})

    # Save to DB (without analysis results yet)
    analysis         = form.save(commit=False)
    analysis.user    = request.user
    analysis.save()

    try:
        # Run NLP pipeline
        pdf_path = analysis.resume_file.path
        results  = analyze_resume(
            pdf_path,
            analysis.job_role,
            analysis.job_description,
        )

        # Update record with results
        analysis.ats_score        = results["ats_score"]
        analysis.match_percentage = results["match_percentage"]
        analysis.matched_keywords = results["matched_keywords"]
        analysis.missing_keywords = results["missing_keywords"]
        analysis.resume_text      = results["resume_text"]
        analysis.word_count       = results["word_count"]
        analysis.save()

        messages.success(request, "✅ Resume analyzed successfully!")
        return redirect("results", pk=analysis.pk)

    except Exception as e:
        analysis.delete()
        messages.error(request, f"Analysis failed: {str(e)}")
        return redirect("home")


@login_required
def results_view(request, pk):
    """Show analysis results."""
    analysis = get_object_or_404(ResumeAnalysis, pk=pk, user=request.user)
    grade, grade_color = analysis.ats_grade
    context = {
        "analysis":   analysis,
        "grade":      grade,
        "grade_color":grade_color,
    }
    return render(request, "analyzer/results.html", context)


@login_required
def history_view(request):
    """Show all past analyses for the user."""
    analyses = ResumeAnalysis.objects.filter(user=request.user)
    return render(request, "analyzer/history.html", {"analyses": analyses})


@login_required
def delete_analysis_view(request, pk):
    """Delete an analysis record."""
    analysis = get_object_or_404(ResumeAnalysis, pk=pk, user=request.user)
    if request.method == "POST":
        # Delete the uploaded file too
        if analysis.resume_file and os.path.exists(analysis.resume_file.path):
            os.remove(analysis.resume_file.path)
        analysis.delete()
        messages.success(request, "Analysis deleted.")
    return redirect("history")
