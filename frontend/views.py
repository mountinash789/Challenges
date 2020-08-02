from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from backend.tasks import get_activities
from backend.views import ActivitiesMixin
from project.utils import LoginRequired
from frontend.forms import LoginForm


class HomePage(LoginRequired, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        get_activities(self.request.user.id)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Dashboard'
        return context


class LoginPage(LoginView):
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Login'
        return context

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse_lazy('front:home')


class ProfilePage(LoginRequired, TemplateView):
    template_name = 'profile.html'
    user = None

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = self.user.get_full_name()
        context['objects'] = [1, 2, 3, 4, 5]
        return context


class ActivitiesPage(ActivitiesMixin, LoginRequired, TemplateView):
    template_name = 'datatables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Activities'
        context['table_id'] = self.__class__.__name__
        context['js_path'] = '/static/js/activities.js'
        context['data_url'] = reverse_lazy('api:activities', kwargs={'user_id': self.request.user.id})
        context['headers'] = [
            'Description',
            'Type',
            'Date',
            'Duration',
            'Distance (Km)',
            'Actions',
        ]
        return context

