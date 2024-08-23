from django.urls import path
from . import views

urlpatterns = [
    path('record/', views.record_attendance, name='record_attendance'),
    path('search/', views.search_attendance, name='search_attendance'),
]
