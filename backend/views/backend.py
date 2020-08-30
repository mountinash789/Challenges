import json
from importlib import import_module

from aog import conv
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Connection
from project.utils import ExactUserRequiredAPI, LoginRequired, best_time_to_run


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


class GoogleAction(APIView):

    def post(self, request, *args, **kwargs):
        res = {}
        queryResult = request.data['queryResult']
        action = queryResult['action']
        if action == 'request_permission':
            res = {
                "payload": {
                    "google": {
                        "expectUserResponse": True,
                        "systemIntent": {
                            "intent": "actions.intent.PERMISSION",
                            "data": {
                                "@type": "type.googleapis.com/google.actions.v2.PermissionValueSpec",
                                "optContext": "To get the weather near you",
                                "permissions": [
                                    "DEVICE_PRECISE_LOCATION"
                                ]
                            }
                        }
                    }
                }
            }
        elif action == 'user_info':
            for context in queryResult['outputContexts']:
                if 'actions_intent_permission' in context['name']:
                    if context['parameters']['PERMISSION']:
                        coords = request.data['originalDetectIntentRequest']['payload']['device']['location'][
                            'coordinates']
                        time = best_time_to_run(coords['longitude'], coords['latitude'])

                        text = 'The best time to go for a run in the next 24 hours is {}'.format(time)
                        res = {
                            "payload": {
                                "google": {
                                    "expectUserResponse": False,
                                    "richResponse": {
                                        "items": [
                                            {
                                                "simpleResponse": {
                                                    "textToSpeech": text,
                                                    "displayText": text
                                                },

                                            },
                                        ]
                                    },
                                }
                            }
                        }
                    else:
                        text = "Unable to get weather. Good Bye"
                        res = {
                            "payload": {
                                "google": {
                                    "expectUserResponse": False,
                                    "richResponse": {
                                        "items": [
                                            {
                                                "simpleResponse": {
                                                    "textToSpeech": text,
                                                    "displayText": text
                                                }
                                            }
                                        ]
                                    },
                                }
                            }
                        }

        return Response(res)
