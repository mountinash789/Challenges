from decimal import Decimal

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, DetailView

from backend.models import Activity, ActivityType
from backend.utils.fitnessscore import FitnessScore
from backend.views.activities import ActivitiesMixin
from project.utils import LoginRequired, start_of_day, end_of_day


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


class ActivitiesFitnessView(ActivitiesMixin, LoginRequired, TemplateView):
    template_name = 'activity/activity-fitness.html'
    start = None
    end = None
    full_qs = None

    def get_initial_queryset(self):
        qs = super().get_initial_queryset()
        qs = qs.filter(date__range=(start_of_day(self.start), end_of_day(self.end)))
        qs = qs.filter(activity_type__description='Run')
        return qs

    def get_data(self):
        labels = []
        data = {'form': [], 'fitness': [], 'fatigue': [], }
        d = self.start
        while d <= self.end:
            fs = FitnessScore(self.user.id, d)

            labels.append(d.strftime("%d/%m/%Y"))
            data['fitness'].append(fs.fitness)
            data['form'].append(fs.form)
            data['fatigue'].append(fs.fatigue)
            d += relativedelta(days=1)
        return labels, data

    def get_context_data(self, **kwargs):
        self.end = timezone.now()
        self.start = self.end - relativedelta(months=1)
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Fitness'
        context['labels'], context['data'] = self.get_data()

        return context
