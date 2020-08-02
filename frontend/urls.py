from django.contrib import admin
from django.urls import path, include

from frontend.views import HomePage, LoginPage, ProfilePage, ActivitiesPage
from django.contrib.auth import views as auth_views

app_name = 'frontend'
urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', HomePage.as_view(), name='home'),
    path('profile/', ProfilePage.as_view(), name='profile'),
    path('activities/', ActivitiesPage.as_view(), name='activities'),
]
