from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.test import TestCase


class ProfileViewTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.test_user.save()
        self.path = reverse_lazy('front:profile')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertRedirects(response, '/login/?next=/profile/')

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)

    def test_users_name(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(str(response.context['page_title']), 'testuser')
        self.assertEqual(response.status_code, 200)

    def test_users_name_with_full_name(self):
        self.test_user.first_name = 'Test'
        self.test_user.last_name = 'User'
        self.test_user.save()

        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(str(response.context['page_title']), 'Test User')
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        test_user.save()
        self.path = reverse_lazy('front:login')

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.path, data={'username': 'testuser', 'password': 'agdusgdiu39u21n'})
        self.assertRedirects(response, reverse_lazy('front:home'))


class ActivitiesViewTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.test_user.save()
        self.path = reverse_lazy('front:activities')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertRedirects(response, '/login/?next=/activities/')

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['data_url'],
                         reverse_lazy('api:activities', kwargs={'user_id': self.test_user.id}))


class RegistrationViewTest(TestCase):

    def setUp(self):
        self.path = reverse_lazy('front:register')

    def test_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(self.path, data={'username': 'created_user', 'password1': 'agdusgdiu39u21n',
                                                     'password2': 'agdusgdiu39u21n'})
        self.assertEqual(User.objects.filter(username='created_user').count(), 1)


class ChallengeCurrentViewTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.test_user.save()
        self.path = reverse_lazy('front:challenge:current')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertRedirects(response, '/login/?next={}'.format(self.path))

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(str(response.context['user']), 'testuser')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['data_url'], reverse_lazy('api:challenge:current'))
