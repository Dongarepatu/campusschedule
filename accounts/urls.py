# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Register page ka URL
    path('register/', views.register, name='register'),
]