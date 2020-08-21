from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView

from backend.models import Activity, ActivityType
from backend.views.activities import ActivitiesMixin
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
