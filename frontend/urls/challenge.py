from django.urls import path

from frontend.views.challenge import PastView, CurrentView

app_name = 'frontend'
urlpatterns = [
    path('current/', CurrentView.as_view(), name='current'),
    path('past/', PastView.as_view(), name='past'),
]
