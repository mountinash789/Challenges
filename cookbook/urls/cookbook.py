from django.urls import path, include

from cookbook.views.api import CookbookData
from cookbook.views.cookbook import CookbookView

app_name = 'cookbook'
urlpatterns = [
    path('', CookbookView.as_view(), name='list'),
    path('api/recipes_data/', CookbookData.as_view(), name='recipes_data'),
]
