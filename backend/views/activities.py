import asyncio

from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django_datatables_view.base_datatable_view import BaseDatatableView
from rest_framework.response import Response

from backend.models import Activity
from backend.tasks import get_activities
from project.utils import ExactUserRequiredAPI, local_time, ExactUserRequired


class ActivitiesMixin(object):
    model = Activity
    user = None

    def get(self, request, *args, **kwargs):
        self.user = self.request.user
        if self.kwargs.get('user_id'):
            self.user = User.objects.get(pk=self.kwargs.get('user_id'))
        return super().get(request, *args, **kwargs)

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
                item.activity_type.description,
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


@api_view()
async def activities_load_async(request, *args, **kwargs):
    user_id = kwargs['user_id']
    loop = asyncio.get_event_loop()
    async_function = sync_to_async(get_activities)
    loop.create_task(async_function(user_id))
    return Response({})
