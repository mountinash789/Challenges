from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.test import TestCase
from model_bakery import baker

from backend.models import UserConnection


class UserConnectionsTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.test_user.save()
        self.test_second_user = User.objects.create_user(username='testotheruser', password='agdusgdiu39u2333n')
        self.test_second_user.save()
        self.path = reverse_lazy('api:user_connections', kwargs={'user_id': self.test_user.id})

    def test_if_not_logged_in(self):
        self.path = reverse_lazy('api:user_connections', kwargs={'user_id': 6000})
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 401)

    def test_logged_in_different_user(self):
        self.path = reverse_lazy('api:user_connections', kwargs={'user_id': self.test_second_user.id})
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 401)

    def test_users_name(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 200)


class ConnectionSignUpViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.connection = baker.make('backend.Connection', library='project.connections.test_connection',
                                     class_str='TestConnection')
        self.user_connection = baker.make('backend.UserConnection', user=self.user, connection=self.connection)
        self.path = reverse_lazy('api:connection_url', kwargs={'user_id': self.user.id, 'pk': self.connection.id})

    def tearDown(self):
        self.user.delete()
        self.connection.delete()
        self.user_connection.delete()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertRedirects(response, '/login/?next={}'.format(self.path))

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 302)


class ConnectionDeauthViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.connection = baker.make('backend.Connection', library='project.connections.test_connection',
                                     class_str='TestConnection')
        self.user_connection = baker.make('backend.UserConnection', user=self.user, connection=self.connection)
        self.path = reverse_lazy('api:connection_deauth', kwargs={'user_id': self.user.id, 'pk': self.connection.id})

    def tearDown(self):
        self.user.delete()
        self.connection.delete()
        self.user_connection.delete()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertRedirects(response, '/login/?next={}'.format(self.path))

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(UserConnection.objects.filter(id=self.user_connection.id).exists())


class ConnectionRedirectViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.connection = baker.make('backend.Connection', library='project.connections.test_connection',
                                     class_str='TestConnection')
        self.path = reverse_lazy('api:connection_redirect', kwargs={'user_id': self.user.id, 'pk': self.connection.id})

    def tearDown(self):
        self.user.delete()
        self.connection.delete()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertRedirects(response, '/login/?next={}'.format(self.path))

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path, {'code': '1'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(UserConnection.objects.filter(user_id=self.user.id).exists())


class ActivitiesListTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.path = reverse_lazy('api:activities', kwargs={'user_id': self.user.id})

    def tearDown(self):
        self.user.delete()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertRedirects(response, '/login/?next={}'.format(self.path))

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recordsTotal'], 0)

    def test_activites_loaded(self):
        activity_type = baker.make('backend.ActivityType')
        baker.make('backend.Activity', user=self.user, activity_type=activity_type, _quantity=3)
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recordsTotal'], 3)


class ActivitiesLoadTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.path = reverse_lazy('api:load_activites', kwargs={'user_id': self.user.id})

    def tearDown(self):
        self.user.delete()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 401)

    def test_logged_in(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
