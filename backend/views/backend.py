from importlib import import_module

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework.response import Response

from backend.models import Connection
from project.utils import ExactUserRequiredAPI, LoginRequired


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
