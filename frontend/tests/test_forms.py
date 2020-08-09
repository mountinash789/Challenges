import django
django.setup()
from django.contrib.auth.models import User
from model_bakery import baker


from django.test import TestCase

from frontend.forms import LoginForm, RegisterForm


class LoginFormTests(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        User.objects.create_user(**self.credentials)

    def test_login(self):
        form = LoginForm(data=self.credentials)
        self.assertTrue(form.is_valid())


class RegisterFormTests(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'testuser',
            'password1': 'Tgbnhy56uJm',
            'password2': 'Tgbnhy56uJm',
        }

    def test_valid_credentials(self):
        form = RegisterForm(data=self.credentials)
        self.assertTrue(form.is_valid())

    def test_invalid_username(self):
        self.credentials['username'] = 'test user'
        form = RegisterForm(data=self.credentials)
        self.assertFalse(form.is_valid())

    def test_non_matching_password(self):
        self.credentials['password1'] = 'Tgbnhy56uJM'
        form = RegisterForm(data=self.credentials)
        self.assertFalse(form.is_valid())

    def test_invalid_password_length(self):
        self.credentials['password1'] = self.credentials['password2'] = 'hunter2'
        form = RegisterForm(data=self.credentials)
        self.assertFalse(form.is_valid())
