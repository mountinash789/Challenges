from django.contrib import admin
from django.urls import path, include

from wedding.views.wedding import HomeView, FunView, VenueView, InputTestView

app_name = 'wedding'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('fun/', FunView.as_view(), name='fun'),
    path('venue/', VenueView.as_view(), name='venue'),
    path('test/input/', InputTestView.as_view(), name='input'),
]
