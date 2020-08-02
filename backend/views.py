from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Connection
from project.utils import ExactUserRequiredAPI


class UserConnections(ExactUserRequiredAPI):
    template_name = 'snippets/connections.html'

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']

        return Response({'id': self.request.GET.get('id', None),
                         'html': render_to_string(self.template_name,
                                                  {'connections': Connection.objects.filter(active=True),
                                                   'user_id': user_id})})
