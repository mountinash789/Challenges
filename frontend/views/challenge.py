from django.urls import reverse_lazy
from django.views.generic import TemplateView

from backend.models import ChallengeSubscription
from backend.views.challenge import ChallengesMixin
from project.utils import LoginRequired, ExactUserRequired


class CurrentView(ChallengesMixin, LoginRequired, TemplateView):
    template_name = 'datatables.html'
    title = 'Current Challenges'
    data_url = 'api:challenge:current'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_header'] = context['page_title'] = self.title
        context['table_id'] = self.__class__.__name__
        context['js_path'] = '/static/js/challenges.js'
        context['data_url'] = reverse_lazy(self.data_url)
        context['headers'] = [
            'Name',
            'Start',
            'End',
            'Instructions',
            'Actions',
        ]
        return context


class PastView(CurrentView):
    title = 'Past Challenges'
    data_url = 'api:challenge:past'


class ChallengeView(ExactUserRequired, TemplateView):
    template_name = 'challenge-view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub'] = ChallengeSubscription.objects.get(challenge_id=self.kwargs['pk'],
                                                           user_id=self.kwargs['user_id'])
        context['page_header'] = context['page_title'] = context['sub'].challenge.name
        return context
