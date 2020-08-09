from dateutil.parser import parse

from backend.models import UserConnection, ActivityType, Activity


class TestConnection(object):
    """
    tets connection library to simulate the tasks to get activites from third parties
    """

    def access_token(self, user_connection_id):
        return 'test_access_token'

    def get_data(self, user_connection_id, all_time=False):
        connection = UserConnection.objects.get(pk=user_connection_id)
        data = [
            {
                'upload_id': 2312312,
                'name': 'Evening Walk',
                'type': 'Walk',
                'start_date': '2020-08-09',
                'elapsed_time': 1200,
                'distance': 1609,
                'total_elevation_gain': 20,
            },
            {
                'upload_id': 2312313,
                'name': 'Evening Run',
                'type': 'Run',
                'start_date': '2020-08-08',
                'elapsed_time': 600,
                'distance': 1609,
                'total_elevation_gain': 20,
            },
        ]
        self.parse_activities(data, connection.user_id)

    @staticmethod
    def get_activity_type(activity_type):
        obj, created = ActivityType.objects.get_or_create(description=activity_type)
        return obj

    def parse_activities(self, activities, user_id):
        for activity in activities:
            obj, created = Activity.objects.get_or_create(
                id=activity['upload_id']
            )
            obj.user_id = user_id
            obj.description = activity['name']
            obj.activity_type = self.get_activity_type(activity['type'])
            obj.date = parse(activity['start_date'])
            obj.duration_seconds = activity['elapsed_time']
            obj.distance_meters = activity['distance']
            obj.total_elevation_gain = activity['total_elevation_gain']
            obj.save()
