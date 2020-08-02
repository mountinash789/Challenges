from django.contrib import admin
from django.urls import path, include

from backend.views import UserConnections

app_name = 'backend'
urlpatterns = [
    path('profile/<int:user_id>/connections/', UserConnections.as_view(), name='user_connections'),
]
