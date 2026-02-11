# timetable/admin.py
from django.contrib import admin
from .models import Department, Faculty, TimetableEntry

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'department']
    list_filter = ['department']
    search_fields = ['name']

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ['department', 'day', 'start_time', 'end_time', 'subject', 'faculty']
    list_filter = ['department', 'day']
    search_fields = ['subject', 'faculty__name']