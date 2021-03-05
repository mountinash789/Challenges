from datetime import date, datetime, timedelta

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, FormView

from backend.models import Activity, ActivityType
from backend.views.activities import ActivitiesMixin
from frontend.forms import ActivityForm, GraphSelectForm
from project.utils import LoginRequired


class ActivitiesPage(ActivitiesMixin, LoginRequired, TemplateView):
    template_name = 'activity/activity-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Activities'
        context['table_id'] = self.__class__.__name__
        context['js_path'] = '/static/js/activities.js'
        context['activity_types'] = ActivityType.objects.all().order_by('description')
        context['data_url'] = reverse_lazy('api:activities:list', kwargs={'user_id': self.request.user.id})
        context['headers'] = [
            'Description',
            'Type',
            'Date',
            'Duration',
            'Distance (Km)',
            'Actions',
        ]
        return context


class ActivityView(LoginRequired, DetailView):
    model = Activity
    template_name = 'activity/view.html'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.user:
            messages.error(request, 'You can only view your own activities!')
            return HttpResponseRedirect(reverse_lazy('front:home'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = self.object.description
        context['activity'] = self.object
        return context


class ActivitiesDistanceView(LoginRequired, TemplateView):
    template_name = 'activity/activity-distance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Distance'
        return context


class ActivitiesFitnessView(LoginRequired, TemplateView):
    template_name = 'activity/activity-fitness.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Fitness'
        return context


class ActivityFormMixin(LoginRequired):
    model = Activity
    template_name = 'base_form.html'
    form_class = ActivityForm
    edit = False

    def form_valid(self, form):
        cleaned = form.cleaned_data
        duration = cleaned['duration']
        delta = datetime.combine(date.min, duration) - datetime.min
        self.object = form.save(commit=False)
        self.object.duration_seconds = delta.total_seconds()
        if not self.edit:
            self.object.user = self.request.user
            self.object.moving_duration_seconds = self.object.duration_seconds
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class AddActivityView(ActivityFormMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Add Activity'
        return context


class EditActivityView(ActivityFormMixin, UpdateView):
    edit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Edit Activity'
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['duration'] = str(timedelta(seconds=int(self.object.duration_seconds)))
        return initial


class ActivitiesGraphs(LoginRequired, FormView):
    template_name = 'activity/graphs.html'
    form_class = GraphSelectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Select Options'
        return context
