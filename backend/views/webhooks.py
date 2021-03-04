from importlib import import_module

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Connection


class HandleConnectionWebhook(APIView):

    def handle(self):
        connection = get_object_or_404(Connection, pk=self.kwargs['pk'])
        module = import_module(connection.library)
        Lib = getattr(module, connection.class_str)
        connect = Lib()
        return connect.handle_webhook(
            {'data': self.request.data,
             'POST': self.request.POST,
             'GET': self.request.GET, })

    def get(self, request, *args, **kwargs):
        data, status = self.handle()
        return Response(data, status=status)

    def post(self, request, *args, **kwargs):
        data, status = self.handle()
        return Response(data, status=status)
