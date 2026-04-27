from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.landing_page, name='landing_page'),
    path('accounts/', include('accounts.urls')),
    path('attendance/', include('attendance.urls')),
    path('dashboards/', include('dashboards.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
