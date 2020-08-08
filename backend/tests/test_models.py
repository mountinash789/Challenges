import django
django.setup()

from datetime import timedelta

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
