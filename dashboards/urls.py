from django.urls import path
from . import views

urlpatterns = [
    path('operativo/', views.operativo_dashboard, name='operativo_dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
]
