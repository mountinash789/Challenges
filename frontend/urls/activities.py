from django.urls import path

from frontend.views.activities import ActivitiesPage, ActivityView, ActivitiesDistanceView, ActivitiesFitnessView

app_name = 'frontend'
urlpatterns = [
    path('', ActivitiesPage.as_view(), name='list'),
    path('<int:pk>/view/', ActivityView.as_view(), name='view'),
    path('distance/', ActivitiesDistanceView.as_view(), name='distance'),
    path('fitness/', ActivitiesFitnessView.as_view(), name='fitness'),
]
