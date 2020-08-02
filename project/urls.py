from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls', namespace='front')),
    path('api/', include('backend.urls', namespace='api')),
]
