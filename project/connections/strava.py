import requests
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone

from backend.models import UserConnection


class Strava(object):

    @staticmethod
    def sign_up(user_id, connection_id):
        return '{}?client_id={}&redirect_uri={}&response_type={}&approval_prompt={}&scope={}'.format(
            settings.STRAVA_AUTH_ENDPOINT,
            settings.STRAVA_CLIENT_ID,
            '{}{}'.format(settings.HOST, reverse_lazy('api:connection_redirect', kwargs={'user_id': user_id,
                                                                                         'pk': connection_id})),
            'code',
            'auto',
            'read_all',
        )

    @staticmethod
    def exchange(user_id, connection_id, code):
        data = {
            'client_id': settings.STRAVA_CLIENT_ID,
            'client_secret': settings.STRAVA_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
        }
        resp = requests.post('https://www.strava.com/oauth/token', data).json()

        obj, created = UserConnection.objects.get_or_create(user_id=user_id, connection_id=connection_id)
        obj.access_token = resp.get('access_token', None)
        obj.refresh_token = resp.get('refresh_token', None)
        obj.expires_at = timezone.now() + relativedelta(seconds=resp.get('expires_in', 0))
        obj.save()

    def refresh(self, user_connection_id):
        connection = UserConnection.objects.get(pk=user_connection_id)
        data = {
            'client_id': settings.STRAVA_CLIENT_ID,
            'client_secret': settings.STRAVA_SECRET,
            'refresh_token': connection.refresh_token,
            'grant_type': 'refresh_token',
        } 
        resp = requests.post('https://www.strava.com/api/v3/oauth/token', data).json()
        connection.access_token = resp.get('access_token', None)
        connection.refresh_token = resp.get('refresh_token', None)
        connection.expires_at = timezone.now() + relativedelta(seconds=resp.get('expires_in', 0))
        connection.save()
        return self.access_token(user_connection_id)

    def access_token(self, user_connection_id):
        connection = UserConnection.objects.get(pk=user_connection_id)
        if connection.expires_at > timezone.now():
            return connection.access_token
        else:
            return self.refresh(user_connection_id)
