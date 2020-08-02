from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView


class RaiseException(object):
    def raise_exception(self):
        return redirect_to_login(self.request.get_full_path(), 'front:login')


class LoginRequired(RaiseException):

    def dispatch(self, request, *args, **kwargs):
        access_denied = []
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
