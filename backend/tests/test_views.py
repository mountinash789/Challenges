from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.test import TestCase
from django.utils import timezone
from model_bakery import baker

from backend.models import UserConnection
from backend.views.challenge import ChallengeGraphic
from project.utils import end_of_day, start_of_day, month_start_end


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


class ChallengesCurrentTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.path = reverse_lazy('api:challenge:current')

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

    def test_challenge_in_future_no_challenges(self):
        start, end = month_start_end(timezone.now() - relativedelta(months=2))
        baker.make('backend.Challenge', start=start, end=end)
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recordsTotal'], 0)

    def test_challenge_in_future_has_challenges(self):
        start, end = month_start_end(timezone.now() + relativedelta(months=2))
        baker.make('backend.Challenge', start=start, end=end)
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recordsTotal'], 1)


class ChallengesPastTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.path = reverse_lazy('api:challenge:past')

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

    def test_challenge_in_future_no_challenges(self):
        start, end = month_start_end(timezone.now() - relativedelta(months=2))
        baker.make('backend.Challenge', start=start, end=end)
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recordsTotal'], 1)

    def test_challenge_in_future_has_challenges(self):
        start, end = month_start_end(timezone.now() + relativedelta(months=2))
        baker.make('backend.Challenge', start=start, end=end)
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['recordsTotal'], 0)


class ChallengesSubscribeTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.challenge = baker.make('backend.Challenge')
        self.path = reverse_lazy('api:challenge:subscribe', kwargs={'user_id': self.user.id, 'pk': self.challenge.id})

    def tearDown(self):
        self.user.delete()
        self.challenge.delete()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 401)

    def test_subscribe(self):
        self.assertEqual(self.challenge.challengesubscription_set.count(), 0)
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 'id_challenge_sub_{}'.format(self.challenge.id))
        self.assertEqual(self.challenge.challengesubscription_set.count(), 1)


class ChallengeGraphicTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='agdusgdiu39u21n')
        self.activity_types = [baker.make('backend.ActivityType')]
        self.challenge = baker.make('backend.Challenge')
        self.path = reverse_lazy('api:challenge:graphic', kwargs={'user_id': self.user.id, 'pk': self.challenge.id})
        baker.make('backend.ChallengeSubscription', user=self.user, challenge=self.challenge)

    def tearDown(self):
        self.user.delete()
        self.challenge.delete()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, 401)

    def test_response_0_activities(self):
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 'id_challenge_status_{}'.format(self.challenge.id))

    def test_response_gte80_activities(self):
        target = [
            baker.make('backend.ChallengeTarget', target_type=baker.make('backend.TargetType', description='Distance',
                                                                         field='distance_meters'),
                       target_value=1000, tracked_activity_type=self.activity_types)]
        dis_challenge = baker.make('backend.Challenge', name='100k Run', targets=target)
        baker.make('backend.ChallengeSubscription', user=self.user, challenge=dis_challenge)
        baker.make('backend.Activity', date=dis_challenge.start, user=self.user,
                   activity_type=self.activity_types[0], distance_meters=1000)
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(
            reverse_lazy('api:challenge:graphic', kwargs={'user_id': self.user.id, 'pk': dis_challenge.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 'id_challenge_status_{}'.format(dis_challenge.id))
        dis_challenge.delete()

    def test_response_gte20_activities(self):
        target = [
            baker.make('backend.ChallengeTarget', target_type=baker.make('backend.TargetType', description='Elevation',
                                                                         field='total_elevation_gain'),
                       target_value=1000, tracked_activity_type=self.activity_types)]
        elev_challenge = baker.make('backend.Challenge', name='100k Run', targets=target)
        baker.make('backend.ChallengeSubscription', user=self.user, challenge=elev_challenge)
        baker.make('backend.Activity', date=elev_challenge.start, user=self.user,
                   activity_type=self.activity_types[0], total_elevation_gain=300)
        login = self.client.login(username='testuser', password='agdusgdiu39u21n')
        response = self.client.get(
            reverse_lazy('api:challenge:graphic', kwargs={'user_id': self.user.id, 'pk': elev_challenge.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 'id_challenge_status_{}'.format(elev_challenge.id))
        elev_challenge.delete()
