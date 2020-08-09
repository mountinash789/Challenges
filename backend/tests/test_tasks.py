from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker

from backend.models import UserConnection, Activity
from backend.tasks import get_activities
from backend.templatetags.model_tags import user_connected


class TaskTestCase(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.connection = baker.make('backend.Connection', library='project.connections.test_connection',
                                     class_str='TestConnection')
        self.user_connection = baker.make('backend.UserConnection', user=self.user, connection=self.connection)

    def tearDown(self):
        self.user.delete()
        self.connection.delete()
        self.user_connection.delete()

    def test_get_activites(self):
        get_activities(self.user.id)
        activities = Activity.objects.filter(user=self.user)

        self.assertEqual(activities.count(), 2)
