from django.contrib.auth import views as auth_views
from django.urls import path, include

from frontend.views.challenge import PastView, CurrentView

app_name = 'frontend'
urlpatterns = [
    path('current/', CurrentView.as_view(), name='current'),
    path('past/', PastView.as_view(), name='past'),
]
