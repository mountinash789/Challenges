from django.urls import path

from backend.views.activities import ActivitiesLoad, ActivitiesList, ActivitiesGetStreams

app_name = 'backend'
urlpatterns = [
    path('<int:user_id>/activities/load/', ActivitiesLoad.as_view(), name='load_activities'),
    path('<int:user_id>/activities/', ActivitiesList.as_view(), name='list'),
    path('<int:pk>/', ActivitiesGetStreams.as_view(), name='get_streams'),
]
