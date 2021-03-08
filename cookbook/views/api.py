from django.utils.safestring import mark_safe
from django_datatables_view.base_datatable_view import BaseDatatableView

from cookbook.models import Recipe
from cookbook.utils.search import search


class CookbookData(BaseDatatableView):
    model = Recipe
    columns = order_columns = ['',
                               'name',
                               '',
                               'cooking_time',
                               '', ]

    def get_initial_queryset(self):
        qs = self.model.objects.all()
        tags = self.request.GET.getlist('selected_tags')
        if len(tags) > 0:
            qs = qs.filter(tags__in=tags)
        return qs

    def filter_queryset(self, qs):
        search_query = self._querydict.get('search[value]', None)
        if len(search_query) > 0:
            return search(search_query, qs)
        return qs

    def prepare_results(self, qs):
        data = []
        for item in qs:
            data.append([
                item.main_image(),
                item.name,
                mark_safe(item.get_tags_display()),
                item.cooking_time_format(),
                '',
            ])

        return data
