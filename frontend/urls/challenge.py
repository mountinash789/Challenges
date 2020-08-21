from django.urls import path

from frontend.views.challenge import PastView, CurrentView, ChallengeView

app_name = 'frontend'
urlpatterns = [
    path('current/', CurrentView.as_view(), name='current'),
    path('past/', PastView.as_view(), name='past'),
    path('<int:pk>/<int:user_id>/view/', ChallengeView.as_view(), name='view'),
]
