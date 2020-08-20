import calendar
import datetime

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse
from django.utils import timezone
from django.utils.timezone import make_aware
from rest_framework.views import APIView


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
