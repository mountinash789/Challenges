from importlib import import_module

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

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

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        connection = get_object_or_404(Connection, pk=self.kwargs['pk'])
        module = import_module(connection.library)
        Lib = getattr(module, connection.class_str)
        connect = Lib()

        return HttpResponseRedirect(connect.sign_up(user.id, connection.pk))


class ConnectionRedirect(LoginRequired, TemplateView):
    template_name = 'snippets/connections.html'

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        connection = get_object_or_404(Connection, pk=self.kwargs['pk'])
        module = import_module(connection.library)
        Lib = getattr(module, connection.class_str)
        connect = Lib()
        connect.exchange(user.id, connection.id, self.request.GET['code'])
        return HttpResponseRedirect(reverse_lazy('front:profile'))
