from django.urls import path

from backend.views.activities import ActivitiesLoad, ActivitiesList, ActivitiesGetStreams, ActivitiesDistance, \
    ActivitiesFitness, ActivitiesGraphData, ActivitiesProgressionData

app_name = 'backend'
urlpatterns = [
    path('<int:user_id>/activities/load/', ActivitiesLoad.as_view(), name='load_activities'),
    path('<int:user_id>/activities/', ActivitiesList.as_view(), name='list'),
    path('<int:pk>/', ActivitiesGetStreams.as_view(), name='get_streams'),
    path('distance/', ActivitiesDistance.as_view(), name='distance'),
    path('fitness/', ActivitiesFitness.as_view(), name='fitness'),
    path('graph_data/', ActivitiesGraphData.as_view(), name='graph_data'),
    path('progression/', ActivitiesProgressionData.as_view(), name='progression'),
]
