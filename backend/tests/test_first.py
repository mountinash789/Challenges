from django.test import TestCase


class FirstTestCase(TestCase):

    def test_is_true(self):
        self.assertTrue(not False)
