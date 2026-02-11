# college_timetable/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Jab koi website khole toh seedha login dikhe
    path('', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Accounts app ke baki urls (register, etc.)
    path('accounts/', include('accounts.urls')),
    
    # Timetable app ke urls
    path('timetable/', include('timetable.urls')),
    
    # Logout functionality
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]