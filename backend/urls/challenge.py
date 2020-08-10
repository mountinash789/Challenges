from django.urls import path

from backend.views.challenge import ChallengesCurrent, ChallengesPast, ChallengeGraphic, ChallengesSubscribe

app_name = 'backend'
urlpatterns = [
    path('current/', ChallengesCurrent.as_view(), name='current'),
    path('past/', ChallengesPast.as_view(), name='past'),
    path('<int:pk>/subscribe/<int:user_id>/', ChallengesSubscribe.as_view(), name='subscribe'),
    path('<int:pk>/graphics/', ChallengeGraphic.as_view(), name='graphic'),
]
