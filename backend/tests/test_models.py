from datetime import timedelta

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from django.test import TestCase
from model_bakery import baker


class ConnectionTestCase(TestCase):

    def setUp(self):
        self.connection = baker.make('backend.Connection', name='Test Name', image_url='https://google.com')

    def tearDown(self):
        self.connection.delete()

    def test_name(self):
        self.assertEqual(self.connection.__str__(), self.connection.name)

    def test_get_image_no_file(self):
        self.assertEqual(self.connection.get_image(), self.connection.image_url)

    def test_get_image_file(self):
        self.connection.image = SimpleUploadedFile("test_image_file.png", b"these are the file contents!")
        self.assertEqual(self.connection.get_image(), self.connection.image.url)


class ActivityTypeTestCase(TestCase):

    def setUp(self):
        self.activity_type = baker.make('backend.ActivityType')

    def tearDown(self):
        self.activity_type.delete()

    def test_description(self):
        self.assertEqual(self.activity_type.__str__(), self.activity_type.description)


class ActivityTestCase(TestCase):

    def setUp(self):
        self.activity = baker.make('backend.Activity')

    def tearDown(self):
        self.activity.delete()

    def test_duration_seconds_formatted(self):
        self.assertEqual(self.activity.duration_seconds_formatted,
                         str(timedelta(seconds=int(self.activity.duration_seconds) or 0)))

    def test_view_button(self):
        html = '<a href="#" class="btn btn-{} btn-primary"><i data-feather="eye"></i> View</a>'.format('sm')
        self.assertEqual(self.activity.view_button(), html)

    def test_truncated_description__gt_20(self):
        self.activity.description = 'This is  a name longer than 20 chars'
        val = '{}...'.format(self.activity.description[:20])
        self.assertEqual(self.activity.truncated_description, val)

    def test_truncated_description__lt_20(self):
        self.activity.description = 'This is  a name'
        self.assertEqual(self.activity.truncated_description, self.activity.description)


class UserConnectionTestCase(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.connection = baker.make('backend.Connection', library='project.connections.test_connection',
                                     class_str='TestConnection')
        self.user_connection = baker.make('backend.UserConnection', user=self.user, connection=self.connection)

    def tearDown(self):
        self.user.delete()
        self.connection.delete()
        self.user_connection.delete()

    def test_get_access_token(self):
        self.assertEqual(self.user_connection.get_access_token(), 'test_access_token')


class TargetTypeTestCase(TestCase):

    def setUp(self):
        self.target_type = baker.make('backend.TargetType', description='Elevation')

    def tearDown(self):
        self.target_type.delete()

    def test_description(self):
        self.assertEqual(self.target_type.__str__(), 'Elevation')


class ChallengeTargetTestCase(TestCase):

    def setUp(self):
        self.challenge_target= baker.make('backend.ChallengeTarget', description='100k Run')

    def tearDown(self):
        self.challenge_target.delete()

    def test_description(self):
        self.assertEqual(self.challenge_target.__str__(), '100k Run')


class ChallengeTestCase(TestCase):

    def setUp(self):
        self.targets_set = baker.make('backend.ChallengeTarget', _quantity=5)
        self.challenge = baker.make('backend.Challenge', name='100k Run', targets=self.targets_set)

    def tearDown(self):
        self.challenge.delete()

    def test_name(self):
        self.assertEqual(self.challenge.__str__(), '100k Run')

    def test_instructions(self):
        html = '<ul>'
        for challenge in self.targets_set:
            html += '<li>{}</li>'.format(challenge.description)
        html += '</ul>'
        self.assertEqual(self.challenge.instructions(), html)


class ChallengeSubscription(TestCase):

    def setUp(self):
        self.user = baker.make(User, first_name='Joe', last_name='Bloggs')
        self.challenge = baker.make('backend.Challenge', name='100k Run')
        self.sub = baker.make('backend.ChallengeSubscription', user=self.user, challenge=self.challenge)

    def tearDown(self):
        self.challenge.delete()

    def test_name(self):
        name = self.sub.__str__()
        self.assertTrue('Joe Bloggs' in name)
        self.assertTrue('100k Run' in name)
