import django
django.setup()
from django.contrib.auth.models import User
from model_bakery import baker


from django.test import TestCase

from frontend.forms import LoginForm


class LoginFormTests(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        form = LoginForm(data=self.credentials)
        self.assertTrue(form.is_valid())
