"""
forms.py — Django Forms
AI Resume Analyzer | Vimal Sahani
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ResumeAnalysis


class ResumeUploadForm(forms.ModelForm):
    """Form to upload resume PDF + job description."""

    class Meta:
        model   = ResumeAnalysis
        fields  = ["resume_file", "job_role", "job_description"]
        widgets = {
            "job_role": forms.TextInput(attrs={
                "class":       "form-control",
                "placeholder": "e.g. Machine Learning Engineer, Data Scientist",
            }),
            "job_description": forms.Textarea(attrs={
                "class":       "form-control",
                "rows":        8,
                "placeholder": "Paste the job description here...",
            }),
            "resume_file": forms.ClearableFileInput(attrs={
                "class":  "form-control",
                "accept": ".pdf",
            }),
        }
        labels = {
            "resume_file":     "Upload Resume (PDF only)",
            "job_role":        "Target Job Role",
            "job_description": "Job Description",
        }

    def clean_resume_file(self):
        file = self.cleaned_data.get("resume_file")
        if file:
            if not file.name.endswith(".pdf"):
                raise forms.ValidationError("Only PDF files are accepted.")
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 5 MB.")
        return file


class CustomRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        "class": "form-control", "placeholder": "Email address"
    }))

    class Meta:
        model  = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
