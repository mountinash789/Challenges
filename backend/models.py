import ast
import datetime
from datetime import timedelta
from decimal import Decimal
from importlib import import_module

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel
from sentry_sdk import capture_exception

from project.utils import percent, what_percent


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
    external_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.connection}"

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

    @property
    def moving_duration_seconds_formatted(self):
        a = timedelta(seconds=int(self.moving_duration_seconds) or 0)
        return str(a)

    def view_button(self, size='sm'):
        return '<a href="{}" class="btn btn-{} btn-primary"><i class="fas fa-eye"></i> View</a>'.format(
            self.get_absolute_url(), size)

    @property
    def truncated_description(self):
        length = 20
        val = self.description
        if val and len(val) > length:
            val = '{}...'.format(val[:length])
        return val

    def distance_km(self):
        return '{}'.format(Decimal(self.distance_meters) / Decimal(1000))

    def get_absolute_url(self):
        return reverse_lazy('front:activities:view', kwargs={'pk': self.id})

    def target_heartrates(self, want_zones=False):
        target = self.user.profile.max_heartrate(self.date)
        target_min = round((55 * target) / 100.0)  # 55% of target
        target_max = round((85 * target) / 100.0)  # 85% of target

        zones = {50: round((50 * target) / 100.0),  # 85% of target
                 60: round((60 * target) / 100.0),  # 85% of target
                 70: round((70 * target) / 100.0),  # 85% of target
                 80: round((80 * target) / 100.0),  # 85% of target
                 90: round((90 * target) / 100.0), }  # 85% of target
        if want_zones:
            return zones
        return target_min, target_max

    def hr_colours(self, hr):
        zones = self.target_heartrates(want_zones=True)
        if hr > zones[90]:
            return 'danger'
        elif hr > zones[80]:
            return 'warning'
        elif hr > zones[70]:
            return 'success'
        elif hr > zones[60]:
            return 'info'
        elif hr > zones[50]:
            return 'secondary'

    def avg_hr_colour(self):
        if self.avg_heart_rate:
            hr = self.avg_heart_rate
            return self.hr_colours(hr)
        return ''

    def pace_mins(self):
        mins = self.moving_duration_seconds / 60
        k = float(self.distance_km())
        pace_mins = 0
        if k != 0:
            pace_mins = float(Decimal(mins) / Decimal(k))
        return pace_mins

    def calc_pace(self):
        pace = datetime.datetime.min + datetime.timedelta(minutes=self.pace_mins())
        self.pace = round(float('{}.{}{}'.format(pace.minute, pace.second, pace.microsecond)), 2)

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    third_party_id = models.CharField(max_length=255, blank=True, null=True)
    external_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    activity_type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    moving_duration_seconds = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    distance_meters = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_elevation_gain = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    latitude = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    longitude = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    avg_heart_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pace = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    polyline = models.TextField(blank=True, null=True)
    raw_json = models.TextField(blank=True, null=True)
    has_streams = models.BooleanField(default=False)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, blank=True, null=True)

    def get_activity_streams(self):
        try:
            if self.connection:
                module = import_module(self.connection.library)
                Lib = getattr(module, self.connection.class_str)
                connect = Lib()
                connect.get_streams(self.connection, self)
                self.has_streams = True
                self.save()
        except Exception as e:
            capture_exception(e)

    def lactate_trimp(self, hr_data):
        score = 0
        data = []
        threshold_1 = self.user.profile.lactate_threshold(1, self.date)
        threshold_2 = self.user.profile.lactate_threshold(2, self.date)
        for rate in hr_data:
            if rate > threshold_2:
                score += 3
            elif threshold_2 > rate > threshold_1:
                score += 2
            elif rate < threshold_1:
                score += 1
            data.append(float(score) / float(self.duration_seconds / 60))
        return data

    def basic_trimp(self, hr_data):
        data = []
        total = len(hr_data)
        for i, rate in enumerate(hr_data, start=1):
            duration = what_percent(percent(i, total), self.duration_seconds)
            score = (duration / 60) * rate
            data.append(float(score) / float(self.duration_seconds / 60))
        return data

    def zonal_trimp(self, hr_data):
        score = 0
        data = []
        total = len(hr_data)
        zones = self.target_heartrates(want_zones=True)
        for i, rate in enumerate(hr_data, start=1):
            if rate >= zones[90]:
                score += 5 * percent(1, total)
            elif rate >= zones[80]:
                score += 4 * percent(1, total)
            elif rate >= zones[70]:
                score += 3 * percent(1, total)
            elif rate >= zones[60]:
                score += 2 * percent(1, total)
            else:
                score += 1 * percent(1, total)
            data.append(float(score) / float(self.duration_seconds / 60))
        return data

    def create_trimp_graphs(self):
        for trimp in ['zonal', 'lactate', 'basic']:
            self.create_trimp_graph(trimp_type=trimp)

    def create_trimp_graph(self, trimp_type):
        if not self.has_streams:
            self.get_activity_streams()
        hr = self.activitystream_set.filter(stream_type__description='heartrate').first()
        trimp_description = 'Trimp {}'.format(trimp_type)
        trimp_stream = self.activitystream_set.filter(stream_type__description=trimp_description).first()
        if hr:
            hr_data = ast.literal_eval(hr.sequence)
            if not trimp_stream:
                stream_type, created = StreamType.objects.get_or_create(description=trimp_description)
                trimp_stream = hr
                trimp_stream.id = None
                trimp_stream.stream_type = stream_type
            data = []

            if trimp_type == 'lactate':
                data = self.lactate_trimp(hr_data)
            elif trimp_type == 'basic':
                data = self.basic_trimp(hr_data)
            elif trimp_type == 'zonal':
                data = self.zonal_trimp(hr_data)

            trimp_stream.sequence = str(data)
            trimp_stream.save()

    def avg_stream_type(self, stream_type_id):
        stream = self.activitystream_set.filter(stream_type_id=stream_type_id).first()
        if stream:
            seq = ast.literal_eval(stream.sequence)
            return sum(seq) / len(seq)
        return 0

    def label_stream(self):
        distance = self.activitystream_set.filter(stream_type__description='distance').first()
        time = self.activitystream_set.filter(stream_type__description='time').first()
        if distance:
            return distance
        else:
            return time

    def has_graphs(self):
        if self.has_streams:
            if self.activitystream_set.filter(stream_type__display_graph=True).count() > 0:
                return True if self.label_stream() else False
        return False

    def save(self, *args, **kwargs):
        if not self.has_streams:
            self.create_trimp_graphs()
        super().save(*args, **kwargs)


class TargetType(TimeStampedModel):
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=20, blank=True, null=True)
    field = models.CharField(max_length=255)

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

    @staticmethod
    def post_save(sender, instance, **kwargs):
        for sub in ChallengeSubscription.objects.filter(challenge=instance):
            sub.save()

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
            return '<span class="id_challenge_sub_{}"><button type="button" data-link="{}" class="btn btn-sm ' \
                   'btn-primary btn-ajax"><i class="fas fa-eye"></i> Join</button><span>'.format(self.id, url)
        return subscriptions.first().get_absolute_url_btn()


class ChallengeSubscription(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('front:challenge:view', kwargs={'pk': self.challenge.id, 'user_id': self.user.id})

    def get_absolute_url_btn(self):
        return '<a href="{}" class="btn btn-sm btn-primary btn-ajax"><i class="fas fa-eye"></i> View</a>'.format(
            self.get_absolute_url())

    def __str__(self):
        return '{} has signed up to {}'.format(self.user.get_full_name(), self.challenge)

    @staticmethod
    def post_save(sender, instance, **kwargs):
        for target in instance.challenge.targets.all():
            obj, created = TargetTracking.objects.get_or_create(subscription=instance, target=target)
            obj.calc()
        return


post_save.connect(Challenge.post_save, sender=Challenge)
post_save.connect(ChallengeSubscription.post_save, sender=ChallengeSubscription)


class TargetTracking(TimeStampedModel):
    subscription = models.ForeignKey(ChallengeSubscription, on_delete=models.CASCADE)
    target = models.ForeignKey(ChallengeTarget, on_delete=models.CASCADE)

    achieved = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    farthest = models.ForeignKey(Activity, blank=True, null=True, related_name='farthest', on_delete=models.SET_NULL)
    highest = models.ForeignKey(Activity, blank=True, null=True, related_name='highest', on_delete=models.SET_NULL)
    fastest = models.ForeignKey(Activity, blank=True, null=True, related_name='fastest', on_delete=models.SET_NULL)
    longest = models.ForeignKey(Activity, blank=True, null=True, related_name='longest', on_delete=models.SET_NULL)

    def percentage(self):
        return round((self.achieved / self.target.target_value) * 100, 0)

    def percentage_class(self):
        prcnt = self.percentage()
        colour_class = 'danger'
        if prcnt > 80:
            colour_class = 'success'
        elif prcnt > 20:
            colour_class = 'warning'
        return colour_class

    def target_value_formatted(self):
        if self.target.target_type.description == 'Elevation':
            target_value = self.target.target_value
        elif self.target.target_type.description == 'Distance':
            target_value = self.target.target_value / Decimal(1000)
        elif self.target.target_type.description == 'Time':
            target_value = str(timedelta(seconds=int(self.target.target_value) or 0))
        else:
            target_value = self.target.target_value
        return target_value

    def achieved_value_formatted(self):
        if self.target.target_type.description == 'Elevation':
            achieved = self.achieved
        elif self.target.target_type.description == 'Distance':
            achieved = self.achieved / Decimal(1000)
        elif self.target.target_type.description == 'Time':
            achieved = str(timedelta(seconds=int(self.achieved) or 0))
        else:
            achieved = self.achieved
        return achieved

    def get_activities(self):
        return Activity.objects.filter(activity_type__in=self.target.tracked_activity_type.all(),
                                       date__range=(self.subscription.challenge.start, self.subscription.challenge.end),
                                       user=self.subscription.user)

    def calc(self):
        activities = self.get_activities()

        self.farthest = activities.order_by('-distance_meters').first()
        self.highest = activities.order_by('-total_elevation_gain').first()
        self.fastest = activities.order_by('pace').first()
        self.longest = activities.order_by('-moving_duration_seconds').first()

        self.achieved = activities.aggregate(total=Sum(self.target.target_type.field))['total'] or 0
        self.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True, help_text='Used to calculate heart rate targets.')

    def __str__(self):
        return self.user.username

    def age(self, ts=None):
        if not ts:
            ts = timezone.now()
        if self.user.profile.dob:
            today = ts
            born = self.user.profile.dob
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return 30

    def max_heartrate(self, ts=None):
        if not ts:
            ts = timezone.now()
        return 220 - self.age(ts)

    def lactate_threshold(self, threshold, ts=None):
        if not ts:
            ts = timezone.now()
        if threshold == 1:
            return 180 - self.age(ts)
        elif threshold == 2:
            return what_percent(87.5, self.max_heartrate(ts))
        return 0

    def get_name(self):
        name = ' '.join(map(str, [self.user.first_name, self.user.last_name]))
        if len(name.strip()) > 0:
            return name
        return self.user


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


class StreamType(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    display_graph = models.BooleanField(default=False)
    rgb = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class ActivityStream(TimeStampedModel):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    stream_type = models.ForeignKey(StreamType, on_delete=models.CASCADE)
    sequence = models.TextField()
    raw_json = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.stream_type.description


class ServiceLog(TimeStampedModel):
    service = models.CharField(max_length=255)
    endpoint = models.CharField(max_length=255)
    sent_data = models.TextField(blank=True, null=True)
    response_data = models.TextField(blank=True, null=True)
