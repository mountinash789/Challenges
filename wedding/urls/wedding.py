from django.contrib import admin
from django.urls import path, include

from wedding.views.wedding import HomeView, FunView, VenueView, InputTestView, RSVPParty, RSVPPin, PrintQR, NameCards, \
    MenuView, RSVPMeal, MealPin, Labels

app_name = 'wedding'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('fun/', FunView.as_view(), name='fun'),
    path('venue/', VenueView.as_view(), name='venue'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('test/input/', InputTestView.as_view(), name='input'),
    path('rsvp/<uuid:party_ref>/', RSVPParty.as_view(), name='rsvp'),
    path('rsvp/pin/', RSVPPin.as_view(), name='rsvp_pin'),
    path('rsvp/print/qr/', PrintQR.as_view(), name='print_qr'),
    path('rsvp/print/name_cards/', NameCards.as_view(), name='name_cards'),
    path('rsvp/print/labels/', Labels.as_view(), name='labels'),
    path('meal/<uuid:party_ref>/', RSVPMeal.as_view(), name='rsvp_meal'),
    path('meal/pin/', MealPin.as_view(), name='menu_pin'),
]
