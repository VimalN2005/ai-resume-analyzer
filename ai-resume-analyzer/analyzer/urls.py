"""
urls.py — Analyzer App URL Routing
AI Resume Analyzer | Vimal Sahani
"""

from django.urls import path
from . import views

urlpatterns = [
    path("",               views.home_view,            name="home"),
    path("analyze/",       views.analyze_view,         name="analyze"),
    path("results/<int:pk>/", views.results_view,      name="results"),
    path("history/",       views.history_view,         name="history"),
    path("delete/<int:pk>/",  views.delete_analysis_view, name="delete_analysis"),
    path("register/",      views.register_view,        name="register"),
    path("login/",         views.login_view,           name="login"),
    path("logout/",        views.logout_view,          name="logout"),
]
