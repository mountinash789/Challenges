from django.urls import path

from backend.views.webhooks import HandleConnectionWebhook

app_name = 'backend'
urlpatterns = [
    path('connection/<int:pk>/', HandleConnectionWebhook.as_view(), name='connection_webhook'),
]
