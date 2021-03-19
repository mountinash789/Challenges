from django_hosts import reverse_lazy
from django.views.generic import TemplateView

from cookbook.models import Tag, Recipe


class CookbookView(TemplateView):
    template_name = 'cookbook/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table_id'] = self.__class__.__name__
        context['js_path'] = '/static/cookbook/js/search.js'
        context['tags'] = Tag.objects.all().order_by('description')
        context['recipes'] = Recipe.objects.all().order_by()
        context['data_url'] = reverse_lazy('recipes_data', host='cookbook')
        context['headers'] = [
            '',
            'Recipe',
            'Tags',
            'Time',
            '',
        ]
        return context


class RecipeView(TemplateView):
    template_name = 'cookbook/recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = Recipe.objects.get(pk=self.kwargs['pk'])
        context['recipe'] = obj
        return context
