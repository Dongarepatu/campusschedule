# timetable/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Main routes
    path('', views.dashboard, name='dashboard'),
    path('departments/', views.department_list, name='department_list'),
    path('department/<int:dept_id>/semesters/', views.department_semesters, name='department_semesters'),
    
    # Timetable routes
   # path('timetable/<int:dept_id>/', views.timetable_view, name='timetable_view'),
    path('<int:dept_id>/', views.timetable_view, name='timetable_view'),
    path('timetable/<int:dept_id>/pdf/', views.download_timetable_pdf, name='download_timetable_pdf'),
    path('entry/create/', views.timetable_create, name='timetable_create'),
    path('entry/delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    
    # Share routes
    path('timetable/<int:dept_id>/share/', views.share_timetable_page, name='share_timetable'),
    path('timetable/<int:dept_id>/share-image/', views.share_timetable_image, name='share_image'),
    
    # Download routes
    path('timetable/<int:dept_id>/excel/', views.download_timetable_excel, name='download_timetable_excel'),
    path('timetable/<int:dept_id>/csv/', views.download_timetable_csv, name='download_timetable_csv'),
    path('timetable/<int:dept_id>/json/', views.download_timetable_json, name='download_timetable_json'),
    path('timetable/<int:dept_id>/word/', views.download_timetable_word, name='download_timetable_word'),
    path('timetable/<int:dept_id>/download/', views.download_all_formats, name='download_all_formats'),
    path('download-image/<int:dept_id>/', views.download_timetable_image, name='download_timetable_image'),
    
    # History routes
    path('department/<int:dept_id>/history/', views.department_history, name='department_history'),
    path('timetable/<int:dept_id>/archive/', views.archive_current_timetable, name='archive_current_timetable'),
    path('history/<int:record_id>/', views.view_history_detail, name='view_history_detail'),
    
    # NEW: Archive search route
    path('archive/search/', views.archive_search, name='archive_search'),

    #delete router
    path('delete-all/<int:dept_id>/', views.delete_all_entries, name='delete_all_entries'),
    path('department/<int:dept_id>/set-active/', views.set_semester_active, name='set_semester_active'),
]