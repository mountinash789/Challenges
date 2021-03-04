from importlib import import_module

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Connection


class HandleConnectionWebhook(APIView):

    def post(self, request, *args, **kwargs):
        connection = get_object_or_404(Connection, pk=self.kwargs['pk'])
        module = import_module(connection.library)
        Lib = getattr(module, connection.class_str)
        connect = Lib()
        data, status = connect.handle_webhook({'data': request.data, 'POST': request.POST, 'GET': request.GET, })
        return Response(data, status=status)
