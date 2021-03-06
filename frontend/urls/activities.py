from django.urls import path

from frontend.views.activities import ActivitiesPage, ActivityView, ActivitiesDistanceView, ActivitiesFitnessView, \
    AddActivityView, EditActivityView, ActivitiesGraphs, Progression

app_name = 'frontend'
urlpatterns = [
    path('', ActivitiesPage.as_view(), name='list'),
    path('add/', AddActivityView.as_view(), name='add'),
    path('<int:pk>/edit/', EditActivityView.as_view(), name='edit'),
    path('<int:pk>/view/', ActivityView.as_view(), name='view'),
    path('distance/', ActivitiesDistanceView.as_view(), name='distance'),
    path('fitness/', ActivitiesFitnessView.as_view(), name='fitness'),
    path('graphs/', ActivitiesGraphs.as_view(), name='graphs'),
    path('progression/', Progression.as_view(), name='progression'),
]
