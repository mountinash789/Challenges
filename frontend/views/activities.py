from django.urls import reverse_lazy
from django.views.generic import TemplateView

from backend.views.activities import ActivitiesMixin
from project.utils import LoginRequired


class ActivitiesPage(ActivitiesMixin, LoginRequired, TemplateView):
    template_name = 'datatables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = 'Activities'
        context['table_id'] = self.__class__.__name__
        context['js_path'] = '/static/js/activities.js'
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
