from django.urls import path, include

from backend.views.backend import UserConnections, ConnectionSignUp, ConnectionRedirect, ConnectionDeAuth, \
    ActivitiesList, ActivitiesLoad

app_name = 'backend'
urlpatterns = [
    path('profile/<int:user_id>/connections/', UserConnections.as_view(), name='user_connections'),
    path('profile/<int:user_id>/connections/<int:pk>/auth/', ConnectionSignUp.as_view(),
         name='connection_url'),
    path('profile/<int:user_id>/connections/<int:pk>/de_auth/', ConnectionDeAuth.as_view(),
         name='connection_deauth'),
    path('profile/<int:user_id>/connections/<int:pk>/redirect/', ConnectionRedirect.as_view(),
         name='connection_redirect'),
    path('<int:user_id>/activities/load/', ActivitiesLoad.as_view(), name='load_activites'),
    path('<int:user_id>/activities/', ActivitiesList.as_view(), name='activities'),
    path('challenge/', include('backend.urls.challenge', namespace='challenge')),
]