from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from project.utils import LoginRequired
from frontend.forms import LoginForm


class HomePage(LoginRequired, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
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
        context['objects'] = [1,2,3,4,5]
        return context
