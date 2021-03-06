from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User

from backend.models import Activity, StreamType
from project.utils import start_of_day, end_of_day


class FitnessScore(object):
    user = None
    date = None

    p = 500
    k1 = 1
    k2 = 2
    t1 = 27
    t2 = 10
    trimp = 100

    fitness = 0
    fatigue = 0
    form = 0
    trimp_type = None

    def __init__(self, user_id, date, trimp_type='basic'):
        self.user = User.objects.get(id=user_id)
        self.date = date
        self.trimp_type = trimp_type
        self.calc()

    @staticmethod
    def weighted_avg(values, weights):
        for g in range(len(values)):
            values[g] = values[g] * weights[g] / sum(weights)
        return sum(values)

    def get_activities_trimp(self, d):
        trimp = 0
        activities = Activity.objects.filter(user=self.user, date__range=(start_of_day(d), end_of_day(d)))
        trimp_description = 'Trimp {}'.format(self.trimp_type)
        trimp_stream = StreamType.objects.filter(description=trimp_description).first()
        for act in activities:
            trimp += act.avg_stream_type(trimp_stream.id)
        if activities.count() > 0:
            trimp = trimp / activities.count()
        return float(trimp)

    def calc_weight(self, d):
        delta = self.date - d
        days = delta.days
        if days > 0:
            return 1 / delta.days
        return 1

    def score(self, days):
        rate = []
        weights = []
        d = self.date - relativedelta(days=days)
        while d <= self.date:
            weights.append(self.calc_weight(d))
            rate.append(self.get_activities_trimp(d))
            d += relativedelta(days=1)

        return self.weighted_avg(rate, weights)

    def calc(self):
        self.fitness = self.score(42)
        self.fatigue = -self.score(7)
        self.form = self.fitness - abs(self.fatigue)
