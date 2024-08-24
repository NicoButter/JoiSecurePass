from django.urls import path
from .views import record_attendance

urlpatterns = [
    #path('record/', views.record_attendance, name='record_attendance'),
    # path('search/', views.search_attendance, name='search_attendance'),
    path('record_attendance/', record_attendance, name='record_attendance'),
    # path('attendance_page/', attendance_page, name='attendance_page'),  # Nueva URL

]
