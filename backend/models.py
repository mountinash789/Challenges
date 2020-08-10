from datetime import timedelta
from importlib import import_module

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from django_extensions.db.models import TimeStampedModel


class Connection(TimeStampedModel):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    connection_url = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=False)
    library = models.CharField(max_length=100, blank=True, null=True)
    class_str = models.CharField(max_length=100, blank=True, null=True)

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url

    def user_connected(self, user_id):
        if self.userconnection_set.filter(user_id=user_id).count() > 0:
            return True
        return False


class UserConnection(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, blank=True, null=True)
    refresh_token = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    last_pulled = models.DateTimeField(blank=True, null=True)

    def get_access_token(self):
        module = import_module(self.connection.library)
        Lib = getattr(module, self.connection.class_str)
        connect = Lib()
        return connect.access_token(self.id)


class ActivityType(TimeStampedModel):
    description = models.CharField(max_length=255, blank=True, null=True)
    icon = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.description


class Activity(TimeStampedModel):

    @property
    def duration_seconds_formatted(self):
        a = timedelta(seconds=int(self.duration_seconds) or 0)
        return str(a)

    def view_button(self, size='sm'):
        return '<a href="#" class="btn btn-{} btn-primary"><i data-feather="eye"></i> View</a>'.format(size)

    @property
    def truncated_description(self):
        length = 20
        val = self.description
        if val and len(val) > length:
            val = '{}...'.format(val[:length])
        return val

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance_meters = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_elevation_gain = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class TargetType(TimeStampedModel):
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.description


class ChallengeTarget(TimeStampedModel):
    description = models.CharField(max_length=255)
    tracked_activity_type = models.ManyToManyField(ActivityType)
    target_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    target_type = models.ForeignKey(TargetType, on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Challenge(TimeStampedModel):
    name = models.CharField(max_length=255)
    targets = models.ManyToManyField(ChallengeTarget)
    start = models.DateTimeField()
    end = models.DateTimeField()

    def __str__(self):
        return self.name

    def instructions(self):
        html = '<ul>'
        for challenge in self.targets.all().order_by('created'):
            html += '<li>{}</li>'.format(challenge.description)
        html += '</ul>'
        return html

    def subscribe_button(self, user_id):
        subscriptions = self.challengesubscription_set.filter(user_id=user_id)
        if subscriptions.count() == 0:
            url = reverse_lazy('api:challenge:subscribe', kwargs={'pk': self.id, 'user_id': user_id})
            return '<span id="id_challenge_sub_{}"><button type="button" data-link="{}" class="btn btn-sm ' \
                   'btn-primary btn-ajax"><i data-feather="eye"></i> Join</button><span>'.format(self.id, url)
        return '<button class="btn btn-sm btn-success disabled"><i data-feather="eye"></i> Joined!</button>'


class ChallengeSubscription(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def __str__(self):
        return '{} has signed up to {}'.format(self.user.get_full_name(), self.challenge)
