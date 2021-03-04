import bugsnag
import requests
from django.utils import timezone

from backend.models import UserConnection, ActivityType, StreamType, ServiceLog


class BaseConnection(object):
    service = None

    @staticmethod
    def sign_up(user_id, connection_id):
        return

    def deauth(self, user_id, connection_id):
        obj = UserConnection.objects.get(user_id=user_id, connection_id=connection_id)
        obj.delete()
        return

    def exchange(self, user_id, connection_id, code):
        pass

    def log(self, endpoint, sent, response):
        l = ServiceLog(
            service=self.service,
            endpoint=endpoint,
            sent_data=sent,
            response_data=response,
        )
        l.save()

    def send(self, endpoint, data, method='POST', headers={}):
        try:
            resp = requests.request(method, endpoint, data=data, headers=headers).json()
        except Exception as e:
            bugsnag.notify(e)
            resp = {}
        self.log(endpoint, data, resp)
        return resp

    def refresh(self, user_connection_id):
        return self.access_token(user_connection_id)

    def access_token(self, user_connection_id):
        connection = UserConnection.objects.get(pk=user_connection_id)
        if connection.expires_at > timezone.now():
            return connection.access_token
        else:
            return self.refresh(user_connection_id)

    def get_data(self, user_connection_id, all_time=False):
        pass

    @staticmethod
    def get_activity_type(activity_type):
        obj, created = ActivityType.objects.get_or_create(description=activity_type)
        return obj

    @staticmethod
    def get_stream_type(stream_type):
        obj, created = StreamType.objects.get_or_create(description=stream_type)
        return obj

    def parse_activities(self, connection, activities, user_id):
        pass

    def get_streams(self, connection, obj):
        pass

    def handle_webhook(self, data):
        self.log('Webhook', {}, data)

        return {}, 200