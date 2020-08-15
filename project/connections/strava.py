import requests
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone

from backend.models import UserConnection, Activity, ActivityType


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
            'activity:read_all',
        )

    @staticmethod
    def deauth(user_id, connection_id):
        obj = UserConnection.objects.get(user_id=user_id, connection_id=connection_id)
        data = {
            'access_token': obj.get_access_token(),
        }
        resp = requests.post('https://www.strava.com/oauth/deauthorize', data).json()
        obj.delete()
        return

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

    def get_data(self, user_connection_id, all_time=False):
        connection = UserConnection.objects.get(pk=user_connection_id)
        endpoint = 'https://www.strava.com/api/v3/athlete/activities'

        data = []
        complete = False
        params = {'per_page': 100, 'page': 1}
        if connection.last_pulled and not all_time:
            params['after'] = connection.last_pulled.timestamp()
        while not complete:
            resp = requests.get(endpoint, params,
                                headers={'Authorization': 'Bearer {}'.format(connection.get_access_token())}).json()
            data.extend(resp)
            if len(resp) == 100:
                params['page'] = params['page'] + 1
                print(params)
            else:
                complete = True
        connection.last_pulled = timezone.now()
        connection.save()

        self.parse_activities(data, connection.user_id)

    @staticmethod
    def get_activity_type(activity_type):
        obj, created = ActivityType.objects.get_or_create(description=activity_type)
        return obj

    def parse_activities(self, activities, user_id):
        for activity in activities:
            obj, created = Activity.objects.get_or_create(
                external_id=activity['upload_id']
            )
            obj.user_id = user_id
            obj.description = activity['name']
            obj.activity_type = self.get_activity_type(activity['type'])
            obj.date = parse(activity['start_date'])
            obj.duration_seconds = activity['elapsed_time']
            obj.distance_meters = activity['distance']
            obj.total_elevation_gain = activity['total_elevation_gain']
            obj.save()
