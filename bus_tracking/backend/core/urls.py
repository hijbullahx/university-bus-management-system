from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('buses/', include('buses.urls')),
    path('schedules/', include('schedules.urls')),
    path('issues/', include('issues.urls')),
    path('notifications/', include('notifications.urls')),
    path('reports/', include('reports.urls')),
    path('locations/', include('locations.urls')),
    path('api/', include('buses.api_urls')),
    path('api/', include('schedules.api_urls')),
    path('api/', include('issues.api_urls')),
    path('api/', include('notifications.api_urls')),
    path('api/', include('reports.api_urls')),
    path('api/', include('locations.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
