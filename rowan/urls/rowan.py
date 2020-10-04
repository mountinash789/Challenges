from django.contrib import admin
from django.urls import path, include

from rowan.views import HomeView

app_name = 'rowan'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]