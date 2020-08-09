from django.urls import path

from backend.views import UserConnections

app_name = 'backend'
urlpatterns = [
    path('current/', UserConnections.as_view(), name='user_connections'),
    path('past/', UserConnections.as_view(), name='user_connections'),
    path('<int:pk>/graphics/', UserConnections.as_view(), name='user_connections'),
]
