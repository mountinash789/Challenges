import json

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone

from backend.models import UserConnection, Activity, ChallengeSubscription, ActivityStream
from project.connections.base import BaseConnection


class Strava(BaseConnection):
    service = 'Strava'

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

    def deauth(self, user_id, connection_id):
        obj = UserConnection.objects.get(user_id=user_id, connection_id=connection_id)
        data = {
            'access_token': obj.get_access_token(),
        }
        self.send('https://www.strava.com/oauth/deauthorize', data)
        obj.delete()
        return

    def exchange(self, user_id, connection_id, code):
        data = {
            'client_id': settings.STRAVA_CLIENT_ID,
            'client_secret': settings.STRAVA_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
        }
        resp = self.send('https://www.strava.com/oauth/token', data)

        obj, created = UserConnection.objects.get_or_create(user_id=user_id, connection_id=connection_id)
        obj.access_token = resp.get('access_token', None)
        obj.refresh_token = resp.get('refresh_token', None)
        athlete = resp.get('athlete', {})
        obj.external_id = athlete.get('id', None)
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
        resp = self.send('https://www.strava.com/api/v3/oauth/token', data)
        connection.access_token = resp.get('access_token', None)
        connection.refresh_token = resp.get('refresh_token', None)
        connection.expires_at = timezone.now() + relativedelta(seconds=resp.get('expires_in', 0))
        connection.save()
        return self.access_token(user_connection_id)

    def get_data(self, user_connection_id, all_time=False):
        connection = UserConnection.objects.get(pk=user_connection_id)
        endpoint = 'https://www.strava.com/api/v3/athlete/activities'

        data = []
        complete = False
        params = {'per_page': 100, 'page': 1}
        if connection.last_pulled and not all_time:
            params['after'] = connection.last_pulled.timestamp()
        while not complete:
            resp = self.send(endpoint, params, method='GET',
                             headers={'Authorization': 'Bearer {}'.format(connection.get_access_token())})
            data.extend(resp)
            if len(resp) == 100:
                params['page'] = params['page'] + 1
                print(params)
            else:
                complete = True
        connection.last_pulled = timezone.now()
        connection.save()

        self.parse_activities(connection, data, connection.user_id)

    def parse_activities(self, connection, activities, user_id):
        for activity in activities:
            obj, created = Activity.objects.get_or_create(
                external_id=activity['upload_id'],
                user_id=user_id,
            )
            obj.third_party_id = activity['id']
            obj.description = activity['name']
            obj.activity_type = self.get_activity_type(activity['type'])
            obj.date = parse(activity['start_date'])
            obj.duration_seconds = activity['elapsed_time']
            obj.moving_duration_seconds = activity['moving_time']
            obj.distance_meters = activity['distance']
            obj.total_elevation_gain = activity['total_elevation_gain']
            if activity.get('average_heartrate', None):
                obj.avg_heart_rate = activity['average_heartrate']
            if activity.get('start_latlng', None):
                obj.latitude = activity['start_latlng'][0]
                obj.longitude = activity['end_latlng'][1]
            if activity.get('map', None):
                obj.polyline = activity['map']['summary_polyline']
            obj.raw_json = json.dumps(activity)
            obj.connection = connection.connection
            obj.calc_pace()
            obj.save()
        if len(activities) > 0:
            for sub in ChallengeSubscription.objects.filter(user_id=user_id):
                sub.save()

    def get_streams(self, connection, obj):
        user_connection = UserConnection.objects.filter(connection=connection, user_id=obj.user_id)
        if user_connection.first():
            endpoint = 'https://www.strava.com/api/v3/activities/{}/streams'.format(obj.third_party_id)
            all_keys = ["time", "latlng", "distance", "altitude", "velocity_smooth", "heartrate", "cadence", "watts",
                        "temp", "moving", "grade_smooth"]

            for stream_type in all_keys:
                params = {'keys': [stream_type], 'key_by_type': True}
                resp = self.send(endpoint, params, method='GET', headers={'Authorization': 'Bearer {}'.format(
                    user_connection.first().get_access_token())})
                if not resp.get('message', None):
                    for key, values in resp.items():
                        stream_obj, created = ActivityStream.objects.get_or_create(
                            activity=obj,
                            stream_type=self.get_stream_type(key),
                            sequence=values['data'],
                            raw_json=json.dumps(values),
                        )

    def get_update_activity(self, user_connection, activity_id):
        endpoint = 'https://www.strava.com/api/v3/activities/{}?include_all_efforts=true'.format(activity_id)
        resp = self.send(endpoint, {}, method='GET',
                         headers={'Authorization': 'Bearer {}'.format(user_connection.get_access_token())})
        self.parse_activities(user_connection, [resp], user_connection.user_id)

    def handle_webhook(self, data):
        super().handle_webhook(data)
        challenge = data['GET'].get('hub.challenge', None)
        if challenge:
            if settings.STRAVA_WEBHOOK_SECRET != data['GET'].get('hub.verify_token', None):
                return {}, 401
            return {"hub.challenge": challenge}, 200

        if data['data']['object_type'] == 'activity':
            connection = UserConnection.objects.get(external_id=data['data']['owner_id'])
            self.get_update_activity(connection, data['data']['object_id'])

        return {}, 200
