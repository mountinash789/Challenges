from importlib import import_module

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django_datatables_view.base_datatable_view import BaseDatatableView
from rest_framework.response import Response

from backend.models import Connection, Activity
from backend.tasks import get_activities
from project.utils import ExactUserRequiredAPI, LoginRequired, ExactUserRequired, local_time


class UserConnections(ExactUserRequiredAPI):
    template_name = 'snippets/connections.html'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        return Response({'id': self.request.GET.get('id', None),
                         'html': render_to_string(self.template_name,
                                                  {'connections': Connection.objects.filter(active=True),
                                                   'user_id': user_id})})


class ConnectionSignUp(LoginRequired, TemplateView):
    template_name = 'snippets/connections.html'
    user = None
    connection = None
    connect = None

    def setup_view(self):
        self.user = get_object_or_404(User, pk=self.kwargs['user_id'])
        self.connection = get_object_or_404(Connection, pk=self.kwargs['pk'])
        module = import_module(self.connection.library)
        Lib = getattr(module, self.connection.class_str)
        self.connect = Lib()

    def get(self, request, *args, **kwargs):
        self.setup_view()
        return HttpResponseRedirect(self.connect.sign_up(self.user.id, self.connection.pk))


class ConnectionDeAuth(ConnectionSignUp):
    def get(self, request, *args, **kwargs):
        self.setup_view()
        self.connect.deauth(self.user.id, self.connection.id)
        return HttpResponseRedirect(reverse_lazy('front:profile'))


class ConnectionRedirect(ConnectionSignUp):

    def get(self, request, *args, **kwargs):
        self.setup_view()
        self.connect.exchange(self.user.id, self.connection.id, self.request.GET['code'])
        return HttpResponseRedirect(reverse_lazy('front:profile'))


class ActivitiesMixin(object):
    model = Activity
    user = None

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        if self.kwargs.get('user_id'):
            self.user = User.objects.get(pk=self.kwargs.get('user_id'))
        return super().get(request, *args, **kwargs)

    def get_initial_queryset(self):
        return self.model.objects.filter(user=self.user)


class ActivitiesList(ActivitiesMixin, ExactUserRequired, BaseDatatableView):
    columns = order_columns = ['description', 'activity_type.description', 'date', 'duration_seconds',
                               'distance_meters', '']

    def prepare_results(self, qs):
        data = []
        for item in qs:
            buttons = [
                '<div class="btn-group btn-group-xs">',
                item.view_button(),
                '</div>',
            ]
            data.append([
                item.truncated_description,
                item.activity_type.description,
                local_time(item.date).strftime('%d/%m/%Y %H:%M:%S'),
                item.duration_seconds_formatted,
                round(item.distance_meters / 1000, 1),
                ''.join(buttons),
            ])

        return data


class ActivitiesLoad(ExactUserRequiredAPI):

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        get_activities(user_id)
        return Response({})
