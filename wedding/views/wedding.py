from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'wedding/home.html'


class FunView(TemplateView):
    template_name = 'wedding/fun.html'


class VenueView(TemplateView):
    template_name = 'wedding/venue.html'


class InputTestView(TemplateView):
    template_name = 'wedding/test/input_tests.html'
