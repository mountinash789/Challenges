from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, FormView, UpdateView

from backend.models import ChallengeSubscription, Profile
from frontend.forms import LoginForm, RegisterForm, ProfileForm
from project.utils import LoginRequired


class HomePage(LoginRequired, TemplateView):
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['page_header'] = context['page_title'] = 'Dashboard'
        context['my_challenges'] = ChallengeSubscription.objects.exclude(challenge__end__lt=now).filter(
            user=self.request.user).order_by('challenge__start')
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


class ProfilePage(LoginRequired, UpdateView):
    template_name = 'profile.html'
    user = None
    model = Profile
    form_class = ProfileForm

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = self.request.user
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.user.profile

    def get_users_name(self):
        full_name = self.user.get_full_name()
        if len(full_name) == 0:
            return self.user.username
        return full_name

    def get_success_url(self):
        messages.success(self.request, 'Profile Updated.')
        return reverse_lazy('front:profile')

    def get_initial(self):
        initial = super().get_initial()
        if self.object.dob:
            initial['dob'] = self.object.dob.strftime('%d/%m/%Y')
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = self.get_users_name()
        context['objects'] = [1, 2, 3, 4, 5]
        return context


class RegistrationView(FormView):
    template_name = 'base_form.html'
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Create an account'
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        url = reverse_lazy('front:profile')
        return url or reverse_lazy('front:home')
