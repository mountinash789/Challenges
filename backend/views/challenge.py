from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Sum
from django.template.loader import render_to_string
from django.utils import timezone
from django_datatables_view.base_datatable_view import BaseDatatableView
from rest_framework.response import Response

from backend.models import Challenge, ChallengeSubscription, Activity, TargetTracking
from project.utils import LoginRequired, ExactUserRequiredAPI, local_time


class ChallengesMixin(object):
    model = Challenge
    user = None
    past = None

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        qs = self.model.objects.filter()
        if self.past:
            qs = qs.filter(end__lt=timezone.now())
        else:
            qs = qs.filter(end__gte=timezone.now())
        return qs


class ChallengesCurrent(ChallengesMixin, LoginRequired, BaseDatatableView):
    past = False
    columns = order_columns = ['name', 'start', 'end', '', '']

    def prepare_results(self, qs):
        data = []
        for item in qs:
            buttons = [
                '<div class="btn-group btn-group-xs">',
                item.subscribe_button(self.user.id),
                '</div>',
            ]
            data.append([
                item.name,
                local_time(item.start).strftime('%d/%m/%Y %H:%M:%S'),
                local_time(item.end).strftime('%d/%m/%Y %H:%M:%S'),
                item.instructions(),
                ''.join(buttons),
            ])

        return data


class ChallengesPast(ChallengesCurrent):
    past = True


class ChallengesSubscribe(ExactUserRequiredAPI):
    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        challenge_id = self.kwargs['pk']
        challenge = Challenge.objects.get(pk=challenge_id)
        obj, created = ChallengeSubscription.objects.get_or_create(
            user=User.objects.get(pk=user_id),
            challenge=challenge,
        )
        return Response({
            'id': 'id_challenge_sub_{}'.format(challenge_id),
            'html': challenge.subscribe_button(user_id),
        })


class ChallengeGraphic(ExactUserRequiredAPI):
    template_name = 'snippets/challenge_graphics.html'
    user = None
    challenge = None

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        challenge_id = self.kwargs['pk']
        self.challenge = Challenge.objects.get(pk=challenge_id)
        self.user = User.objects.get(pk=user_id)
        sub = ChallengeSubscription.objects.get(user=self.user, challenge=self.challenge)
        return Response({
            'id': 'id_challenge_status_{}'.format(challenge_id),
            'html': render_to_string(self.template_name, {'user': self.user, 'challenge': self.challenge,
                                                          'target_data': TargetTracking.objects.filter(
                                                              subscription=sub)}),
        })
