from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker

from backend.models import UserConnection
from backend.templatetags.model_tags import user_connected


class ModelTagsTestCase(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.connection = baker.make('backend.Connection')

    def tearDown(self):
        self.user.delete()
        self.connection.delete()

    def test_user_connected(self):
        u = UserConnection(user=self.user, connection=self.connection)
        u.save()
        self.assertTrue(user_connected(self.connection, self.user.id))

    def test_user_not_connected(self):
        self.assertFalse(user_connected(self.connection, self.user.id))
