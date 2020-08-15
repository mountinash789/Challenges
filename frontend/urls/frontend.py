from django.contrib.auth import views as auth_views
from django.urls import path, include

from frontend.views.frontend import HomePage, LoginPage, ProfilePage, ActivitiesPage, RegistrationView

app_name = 'frontend'
urlpatterns = [
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('', include('social_django.urls', namespace='social')),
    path('', HomePage.as_view(), name='home'),
    path('profile/', ProfilePage.as_view(), name='profile'),
    path('activities/', ActivitiesPage.as_view(), name='activities'),
    path('challenge/', include('frontend.urls.challenge', namespace='challenge')),
]
