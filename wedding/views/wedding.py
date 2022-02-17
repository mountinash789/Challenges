import bugsnag
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import TemplateView
from django_hosts import reverse_lazy

from project.utils import send_email, LoginRequired
from wedding.models import Party, DietaryReq, Guest, Starter, Main, Dessert
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


class MealPin(TemplateView):
    template_name = 'wedding/rsvp-pin.html'
    error = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['error'] = self.request.GET.get('e', False)
        return context

    def post(self, request, *args, **kwargs):
        try:
            party = Party.objects.get(pin=self.request.POST['pin'])
            return HttpResponseRedirect(party.get_meal_url())
        except Exception as e:
            pass
        return HttpResponseRedirect(reverse_lazy('meal_pin', host='wedding') + '?e=1')


class PrintQR(TemplateView):
    template_name = 'wedding/test/qr_codes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['parties'] = Party.objects.all()
        return context


class NameCards(TemplateView):
    template_name = 'wedding/test/name_cards.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        guests = Guest.objects.filter(attending=True)
        start = int(self.request.GET.get('start', 0))
        max = int(self.request.GET.get('max', 100000))
        context['guests'] = guests[start:start + max]
        return context


class MenuView(TemplateView):
    template_name = 'wedding/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['starters'] = Starter.objects.filter(active=True)
        context['mains'] = Main.objects.filter(active=True)
        context['desserts'] = Dessert.objects.filter(active=True)
        return context


class RSVPMeal(TemplateView):
    template_name = 'wedding/rsvp_meal.html'
    party = None

    def get(self, request, *args, **kwargs):
        self.party = get_object_or_404(Party, reference=self.kwargs['party_ref'])
        self.party.last_accessed = timezone.now()
        self.party.save()

        if not settings.CAN_CHANGE_MEAL_CHOICE:
            messages.error(self.request, 'You can no longer change your meal choice.')
            return HttpResponseRedirect(reverse_lazy('home', host='wedding'))

        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.party = get_object_or_404(Party, reference=self.kwargs['party_ref'])
            self.party.save()

            for guest in self.party.guests().filter(attending=True):
                starter_id = self.request.POST.get('{}_starter_id'.format(guest.id), None)
                main_id = self.request.POST.get('{}_main_id'.format(guest.id), None)
                dessert_id = self.request.POST.get('{}_dessert_id'.format(guest.id), None)
                guest.starter_id = starter_id
                guest.main_id = main_id
                guest.dessert_id = dessert_id
                guest.save()

            send_email('Meal Option Responded',
                       render_to_string('wedding/guest_meals_email.html', {'party': self.party}), settings.OUR_EMAILS,
                       html=True)
            messages.success(self.request, 'Thank you for submitting. Your response has been saved.', )
        except Exception as e:
            messages.error(self.request, 'An error occurred. It has been logged, please try later.')
            bugsnag.notify(e)
        return HttpResponseRedirect(reverse_lazy('home', host='wedding'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['party'] = self.party
        context['guests'] = self.party.guests().filter(attending=True).order_by('sequence')
        context['starters'] = Starter.objects.filter(active=True)
        context['mains'] = Main.objects.filter(active=True)
        context['desserts'] = Dessert.objects.filter(active=True)
        return context


class Labels(TemplateView):
    template_name = 'wedding/test/labels.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        labels = ["Apple Crumble", "Chocolate", "Coffee", "Red Velvet", "Sticky Toffee", "Vegan Chocolate", "Victoria",
                  "Elizabeth"]
        context['labels'] = labels
        return context
