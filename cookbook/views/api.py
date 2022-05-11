from django.core import serializers
from django.utils.safestring import mark_safe
from django_datatables_view.base_datatable_view import BaseDatatableView
from rest_framework.response import Response
from rest_framework.views import APIView

from cookbook.models import Recipe
from cookbook.serialisers import RecipeSerializer
from cookbook.utils.search import search


class CookbookData(APIView):
    model = Recipe

    def get_initial_queryset(self):
        qs = self.model.objects.all()
        tags = self.request.GET.getlist('selected_tags[]')
        if len(tags) > 0:
            for tag in tags:
                qs = qs.filter(tags__in=tag)
        return qs

    def filter_queryset(self, qs):
        search_query = self.request.GET.get('search', '')
        if len(search_query) > 0:
            return search(search_query, qs)
        return qs

    def get(self, request, *args, **kwargs):
        qs = self.get_initial_queryset()
        qs = self.filter_queryset(qs)
        serializer = RecipeSerializer(qs, many=True)
        return Response({'count': qs.count(), 'cards': serializer.data})
