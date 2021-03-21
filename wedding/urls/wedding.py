from django.contrib import admin
from django.urls import path, include

from wedding.views.wedding import HomeView, FunView, VenueView, InputTestView, RSVPParty, RSVPPin, PrintQR

app_name = 'wedding'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('fun/', FunView.as_view(), name='fun'),
    path('venue/', VenueView.as_view(), name='venue'),
    path('test/input/', InputTestView.as_view(), name='input'),
    path('rsvp/<uuid:party_ref>/', RSVPParty.as_view(), name='rsvp'),
    path('rsvp/pin/', RSVPPin.as_view(), name='rsvp_pin'),
    path('rsvp/print/qr/', PrintQR.as_view(), name='print_qr'),
]
