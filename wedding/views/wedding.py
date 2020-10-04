import bugsnag
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView
from django_hosts import reverse_lazy
from wedding.models import Party, DietaryReq
from django.contrib import messages


class HomeView(TemplateView):
    template_name = 'wedding/home.html'


class FunView(TemplateView):
    template_name = 'wedding/fun.html'


class VenueView(TemplateView):
    template_name = 'wedding/venue.html'


class InputTestView(TemplateView):
    template_name = 'wedding/test/input_tests.html'


class RSVPParty(TemplateView):
    template_name = 'wedding/rsvp.html'
    party = None

    def get(self, request, *args, **kwargs):
        self.party = get_object_or_404(Party, reference=self.kwargs['party_ref'])
        self.party.last_accessed = timezone.now()
        self.party.save()
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.party = get_object_or_404(Party, reference=self.kwargs['party_ref'])
            self.party.phone_number = self.request.POST.get('phone_number', None)
            self.party.email_address = self.request.POST.get('email_address', None)
            self.party.attending = True if self.request.POST.get('attending', False) == 'Yes' else False
            self.party.rsvp_responded = True

            if self.party.offering_hotel_room:
                self.party.wants_hotel_room = True if self.request.POST.get('hotel_room', False) == 'Yes' else False
            if self.party.offering_hotel_room_day_before:
                self.party.wants_hotel_room = True if self.request.POST.get('hotel_room_night_before',
                                                                            False) == 'Yes' else False
            self.party.save()

            for guest in self.party.guests():
                dietary = self.request.POST.getlist('{}_dietary_req'.format(guest.id), [])
                if len(dietary) > 0:
                    guest.dietary_requirements.set(dietary)

            messages.success(self.request, 'Thank you for submitting. Your response has been saved.')
        except Exception as e:
            messages.error(self.request, 'An error occurred. It has been logged, please try later.')
            bugsnag.notify(e)
        return HttpResponseRedirect(reverse_lazy('home', host='wedding'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['party'] = self.party
        context['guests'] = self.party.guests()
        context['dietary_reqs'] = DietaryReq.objects.all()
        return context
