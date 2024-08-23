from django.urls import path
from . import views
# from attendance import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('personal_registration/', views.personal_registration, name='personal_registration'),
    # path('record_attendance/', views.record_attendance, name='record_attendance'),
]
