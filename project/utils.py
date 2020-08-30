import calendar
import datetime

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework.views import APIView

from backend.models import Weather


class RaiseException(object):
    def raise_exception(self):
        return redirect_to_login(self.request.get_full_path(), 'front:login')


class LoginRequired(RaiseException):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You are not logged in!')
            return redirect_to_login(request.get_full_path(), 'front:login')
        return super().dispatch(request, *args, **kwargs)


class ExactUserRequired(RaiseException):
    user_key = 'user_id'

    def dispatch(self, request, *args, **kwargs):
        user_id = self.kwargs.get(self.user_key, 0)
        if user_id != self.request.user.id:
            return self.raise_exception()
        return super().dispatch(request, *args, **kwargs)


class ExactUserRequiredAPI(ExactUserRequired, APIView):
    def raise_exception(self):
        return HttpResponse(status=401)


def local_time(dt):
    return timezone.localtime(dt)


def start_of_day(dt):
    return make_aware(datetime.datetime.combine(dt, datetime.time.min))


def end_of_day(dt):
    return make_aware(datetime.datetime.combine(dt, datetime.time.max))


def month_start_end(dt):
    first_day = dt.date().replace(day=1)
    last_day = dt.date().replace(day=calendar.monthrange(dt.date().year, dt.date().month)[1])
    return start_of_day(first_day), end_of_day(last_day)


def get_and_store_next_48hours_weather_info(long, lat):
    start = timezone.now() + relativedelta(minute=0, second=0)
    end = start + relativedelta(hours=24)
    w = Weather.objects.filter(longitude=long, latitude=lat, timestamp__range=(start, end))
    if w.count() < 24:
        from project.libs.open_weather import OpenWeather
        weather_lib = OpenWeather(long, lat)
        weather_lib.save_hourly_weather()
        w = Weather.objects.filter(longitude=long, latitude=lat, timestamp__range=(start, end))
    return w


def best_time_to_run(long, lat):
    next_24_hour_weather = get_and_store_next_48hours_weather_info(long, lat)
    optimal_weather_ranges = {
        'temperature': (10, 18),
        'feels_like': (10, 17),
        'pressure': (10, 15),
        'humidity': (0, 73),
        'dew_point': (10, 15),
        'clouds': (10, 15),
        'visibility': (10, 15),
        'wind_speed': (0, 20),
        'wind_deg': (10, 15),
    }

    start = timezone.now()
    end = start + relativedelta(hours=24)
    filtered = next_24_hour_weather.filter(
        feels_like__range=optimal_weather_ranges['feels_like'],
        humidity__range=optimal_weather_ranges['humidity'],
        wind_speed__range=optimal_weather_ranges['wind_speed'],
        timestamp__range=(start, end),
        timestamp__hour__range=(8, 19),
    )
    if filtered.count() > 0:
        first = filtered.first().timestamp
        if all([first.date() == timezone.localtime().date(),
                first.hour == timezone.localtime().hour]):
            return 'NOW! GO! GO! GO!'

        return first.strftime('%A, %B %e at %I:%M %p')
    return 'Not Today!'
