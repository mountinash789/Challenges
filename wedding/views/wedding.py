import bugsnag
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView
from django_hosts import reverse_lazy

from project.utils import send_email
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
            # self.party.attending = True if self.request.POST.get('attending', False) == 'Yes' else False
            self.party.rsvp_responded = True

            if self.party.offering_hotel_room:
                self.party.wants_hotel_room = True if self.request.POST.get('hotel_room', False) == 'Yes' else False
            if self.party.offering_hotel_room_day_before:
                self.party.wants_hotel_room_day_before = True if self.request.POST.get('hotel_room_night_before',
                                                                                       False) == 'Yes' else False
            self.party.save()

            for guest in self.party.guests():
                dietary_req = self.request.POST.get('{}_dietary_req'.format(guest.id), None)
                guest.dietary_requirements_text = dietary_req
                guest.attending = True if self.request.POST.get('{}_attending'.format(guest.id),
                                                                False) == 'Yes' else False
                if guest.is_plus_one:
                    guest_name = self.request.POST.get('{}_guest_name'.format(guest.id), 'none').split(' ', 1)
                    last = guest.surname
                    first = guest_name[0]
                    if len(guest_name) > 1:
                        last = guest_name[1]
                    guest.first_name = first
                    guest.surname = last
                guest.save()

            send_email('RSVP Responded', '{} party has responded.'.format(self.party.description), settings.OUR_EMAILS)
            messages.success(self.request, 'Thank you for submitting. Your response has been saved.')
        except Exception as e:
            messages.error(self.request, 'An error occurred. It has been logged, please try later.')
            bugsnag.notify(e)
        return HttpResponseRedirect(reverse_lazy('home', host='wedding'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['party'] = self.party
        context['guests'] = self.party.guests().order_by('sequence')
        context['dietary_reqs'] = DietaryReq.objects.all()
        return context


class RSVPPin(TemplateView):
    template_name = 'wedding/rsvp-pin.html'
    error = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['error'] = self.request.GET.get('e', False)
        return context

    def post(self, request, *args, **kwargs):
        try:
            party = Party.objects.get(pin=self.request.POST['pin'])
            return HttpResponseRedirect(party.get_absolute_url())
        except Exception as e:
            pass
        return HttpResponseRedirect(reverse_lazy('rsvp_pin', host='wedding') + '?e=1')
