from django.conf import settings
from django.conf.global_settings import STATIC_ROOT
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include('Online_App.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)