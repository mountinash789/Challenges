from django_hosts import reverse_lazy
from django.views.generic import TemplateView


class CookbookView(TemplateView):
    template_name = 'cookbook/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['page_header'] = context['page_title'] = 'Activities'
        context['table_id'] = self.__class__.__name__
        context['js_path'] = '/static/cookbook/js/search.js'
        # context['activity_types'] = ActivityType.objects.all().order_by('description')
        context['data_url'] = reverse_lazy('recipes_data', host='cookbook')
        context['headers'] = [
            '',
            'Recipe',
            'Tags',
            'Time',
            '',
        ]
        return context
