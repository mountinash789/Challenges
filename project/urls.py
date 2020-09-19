from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls.frontend', namespace='front')),
    path('api/', include('backend.urls.backend', namespace='api')),
    # path('wedding/', include('wedding.urls.wedding', namespace='wedding')),
    # path('rowan/', include('rowan.urls.rowan', namespace='wedding')),
]
