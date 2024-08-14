from django.urls import path
from . import views

urlpatterns = [
    path('register/admin/', views.register_administrador, name='register_admin'),
    path('register/personal/', views.register_personal, name='register_personal'),
]
