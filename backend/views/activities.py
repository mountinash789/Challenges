from datetime import timedelta
from itertools import accumulate

from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.template.loader import render_to_string
from django.utils import timezone
from django_datatables_view.base_datatable_view import BaseDatatableView
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Activity, ActivityType
from backend.tasks import get_activities
from backend.utils.fitnessscore import FitnessScore
from project.utils import ExactUserRequiredAPI, local_time, ExactUserRequired, LoginRequired, start_of_day, end_of_day, \
    week_end, week_start


class ActivitiesMixin(object):
    model = Activity
    user = None

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        if self.kwargs.get('user_id'):
            self.user = User.objects.get(pk=self.kwargs.get('user_id'))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.user = self.request.user
        if self.kwargs.get('user_id'):
            self.user = User.objects.get(pk=self.kwargs.get('user_id'))
        return super().post(request, *args, **kwargs)

    def get_initial_queryset(self):
        return self.model.objects.filter(user=self.user)


class ActivitiesList(ActivitiesMixin, ExactUserRequired, BaseDatatableView):
    columns = order_columns = ['description', 'activity_type.description', 'date', 'duration_seconds',
                               'distance_meters', '']

    def prepare_results(self, qs):
        data = []
        for item in qs:
            buttons = [
                '<div class="btn-group btn-group-xs">',
                item.view_button(),
                '</div>',
            ]
            data.append([
                item.truncated_description,
                item.activity_type.description if item.activity_type else '',
                local_time(item.date).strftime('%d/%m/%Y %H:%M:%S'),
                item.duration_seconds_formatted,
                round(item.distance_meters / 1000, 1),
                ''.join(buttons),
            ])

        return data


class ActivitiesLoad(ExactUserRequiredAPI):

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        get_activities(user_id)
        return Response({})


class ActivitiesGetStreams(LoginRequired, APIView):

    def get(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs['pk'])
        activity.get_activity_streams()
        activity = Activity.objects.get(id=kwargs['pk'])
        return Response({'has_graphs': activity.has_graphs(),
                         'html': render_to_string('snippets/graphs.html', {'activity': activity})})


class ActivitiesDistance(ActivitiesMixin, LoginRequired, APIView):
    start_date = None
    end_date = None
    current_date = None
    labels = []
    data = []
    dates = []
    current = {}

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        self.start_date = self.request.GET.get('start_date', None)
        self.end_date = self.request.GET.get('end_date', None)
        self.current_date = self.request.GET.get('current', None)
        if self.start_date:
            self.start_date = parse(self.start_date)
        else:
            self.start_date = timezone.now() - relativedelta(weeks=11)

        if self.end_date:
            self.end_date = parse(self.end_date)
        else:
            self.end_date = timezone.now()

        self.start_date = week_start(self.start_date)
        self.end_date = week_end(self.end_date)

        if self.current_date and self.current_date != '0':
            self.current_date = parse(self.current_date)
        else:
            self.current_date = week_start(self.end_date)

        self.current = {
            'date_range': "{} - {}".format(
                week_start(self.current_date).strftime('%d/%m/%Y'),
                week_end(self.current_date).strftime('%d/%m/%Y'), ),
            'distance': 0,
            'elevation': 0,
            'time': 0,
        }

        self.get_data()
        return Response({
            'labels': self.labels,
            'dates': self.dates,
            'data': self.data,
            'current': self.current,
        })

    def get_data(self):
        self.labels = []
        self.data = []
        self.dates = []
        qs = self.get_initial_queryset()
        d = self.start_date
        month = None
        while d < self.end_date:
            new_month = d.strftime('%B')
            if month != new_month:
                month = d.strftime('%B')
                self.labels.append(month)
            else:
                self.labels.append('')
            activities = qs.filter(date__range=(week_start(d), week_end(d))).aggregate(
                Sum('distance_meters'), Sum('total_elevation_gain'), Sum('duration_seconds'))
            value = activities.get('distance_meters__sum', None) or 0
            self.data.append(value / 1000)
            self.dates.append(week_start(d).strftime('%Y-%m-%d'))
            if week_start(d).date() == self.current_date.date():
                self.current['distance'] = value / 1000
                self.current['elevation'] = activities.get('total_elevation_gain__sum', None) or 0
                duration = timedelta(seconds=int(activities.get('duration_seconds__sum', None) or 0) or 0)
                self.current['time'] = str(duration)

            d = week_end(d) + relativedelta(days=1)

    def get_initial_queryset(self):
        qs = super().get_initial_queryset()
        qs = qs.filter(date__range=(start_of_day(self.start_date), end_of_day(self.end_date)))
        qs = qs.filter(activity_type__description='Run')
        return qs


class ActivitiesFitness(ActivitiesMixin, LoginRequired, APIView):
    start = None
    end = None
    activity_types = None

    def post(self, request, *args, **kwargs):
        self.user = self.request.user
        self.end = end_of_day(parse(self.request.POST['end']))
        self.start = start_of_day(parse(self.request.POST['start']))
        self.activity_types = ActivityType.objects.filter(id__in=self.request.POST.getlist("activity_type"))
        labels, data = self.get_data()
        return Response({
            'labels': labels,
            'data': data,
        })

    def get_data(self):
        labels = []
        data = {'form': [], 'fitness': [], 'fatigue': [], }
        d = self.start
        while d <= self.end:
            fs = FitnessScore(self.user.id, d, self.request.GET.get('type', None))
            labels.append(d.strftime("%d/%m/%Y"))
            data['fitness'].append(fs.fitness)
            data['form'].append(fs.form)
            data['fatigue'].append(fs.fatigue)
            d += relativedelta(days=1)
        return labels, data

    def get_initial_queryset(self):
        qs = super().get_initial_queryset()
        qs = qs.filter(date__range=(start_of_day(self.start), end_of_day(self.end)),
                       activity_type__in=self.activity_types)
        return qs


class ActivitiesGraphData(ActivitiesMixin, LoginRequired, APIView):
    start = None
    end = None
    activity_types = None
    data_points = None

    def post(self, request, *args, **kwargs):
        self.user = self.request.user
        self.end = end_of_day(parse(self.request.POST['end']))
        self.start = start_of_day(parse(self.request.POST['start']))
        self.activity_types = ActivityType.objects.filter(id__in=self.request.POST.getlist("activity_type"))
        self.data_points = self.request.POST.getlist("data_points")
        labels, data = self.get_data()
        return Response({
            'labels': labels,
            'data': data,
        })

    def get_data(self):
        labels = []
        data = {k: [] for k in self.data_points}
        d = self.start
        base_qs = self.get_initial_queryset()
        while d <= self.end:
            day_qs = base_qs.filter(date__range=(start_of_day(d), end_of_day(d)))
            if 'Duration' in self.data_points:
                data['Duration'].append(day_qs.aggregate(Sum('duration_seconds'))['duration_seconds__sum'])
            if 'Pace' in self.data_points:
                data['Pace'].append(day_qs.aggregate(Sum('pace'))['pace__sum'])
            labels.append(d.strftime("%d/%m/%Y"))
            d += relativedelta(days=1)
        return labels, data

    def get_initial_queryset(self):
        qs = super().get_initial_queryset()
        qs = qs.filter(date__range=(self.start, self.end), activity_type__in=self.activity_types)
        return qs


class ActivitiesProgressionData(ActivitiesMixin, LoginRequired, APIView):
    start = None
    end = None
    activity_types = None
    data_points = None

    def min_year(self):
        oldest = Activity.objects.filter(user=self.user, activity_type__in=self.activity_types).exclude(
            date=None).order_by('date').first()
        if not oldest:
            return timezone.now().year
        return oldest.date.year

    def post(self, request, *args, **kwargs):
        self.user = self.request.user
        self.end = end_of_day(parse(self.request.POST['end']))
        self.start = start_of_day(parse(self.request.POST['start']))
        self.activity_types = ActivityType.objects.filter(id__in=self.request.POST.getlist("activity_type"))
        self.data_point = self.request.POST["type"]
        labels, data = self.get_data()
        return Response({
            'labels': labels,
            'data': data,
        })

    def get_data(self):
        now = timezone.now()
        this_year = now.year
        years = list(range(self.min_year(), this_year + 1))
        labels = []
        data = {str(k): [] for k in years}
        d = self.start
        while d <= self.end:
            for year in data.keys():
                qs = self.get_qs(d, int(year))
                if year == str(this_year) and d > now:
                    continue
                data[year].append(qs.get(self.data_point, 0) or 0)
            labels.append(d.strftime("%d/%m"))
            d += relativedelta(days=1)
        for k, v in data.items():
            data[k] = list(accumulate(v))
        return labels, data

    def get_qs(self, date, year):
        start = start_of_day(date + relativedelta(year=year))
        end = end_of_day(start)
        qs = super().get_initial_queryset()
        qs = qs.filter(
            date__range=(start, end),
            activity_type__in=self.activity_types
        ).aggregate(
            Sum('distance_meters'),
            Sum('duration_seconds'),
            Sum('total_elevation_gain'),
            Count('id'),
        )
        return qs
