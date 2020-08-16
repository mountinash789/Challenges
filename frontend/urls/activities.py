from django.urls import path

from frontend.views.activities import ActivitiesPage

app_name = 'frontend'
urlpatterns = [
    path('', ActivitiesPage.as_view(), name='list'),
    path('<int:pk>/view/', ActivitiesPage.as_view(), name='view'),
]
