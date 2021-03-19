from django.db import models
from django.db.models import Index, UniqueConstraint, Q
from django.utils.safestring import mark_safe
from django_extensions.db.models import TimeStampedModel
from django_hosts import reverse_lazy

from cookbook.utils.search import generate_keywords


class Tag(TimeStampedModel):
    description = models.CharField(max_length=255)
    colour = models.CharField(max_length=255)
    text_color = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    def html(self):
        return '<span class="badge" style="background-color:{};color:{}">{}</span>'.format(
            self.colour, self.text_color, self.description
        )


class Item(TimeStampedModel):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Unit(TimeStampedModel):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class Recipe(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    cooking_time = models.TimeField()

    def __str__(self):
        return self.name

    def cooking_time_format(self):
        hour = self.cooking_time.hour
        minute = self.cooking_time.minute
        text = []
        if hour > 0:
            text.append('{} hour{}'.format(hour, 's' if hour > 1 else ''))
        if minute > 0:
            text.append('{} minute{}'.format(minute, 's' if minute > 1 else ''))

        return ' and '.join(text)

    def get_absolute_url(self):
        return reverse_lazy('view', kwargs={'pk': self.id}, host='cookbook')

    def html_name(self):
        return mark_safe('<b>{}</b><p>{}</p>'.format(self.name, self.description))

    def get_tags_display(self):
        tag_html = ''
        for tag in self.tags.all():
            tag_html += tag.html()

        return tag_html

    def main_image(self):
        image = self.recipeimage_set.filter(main=True).first()
        if image:
            return '<img src="{}"></img>'.format(image.photo.url)
        return ''

    def generate_index(self):
        name_keywords = generate_keywords(self.name)
        description_keywords = generate_keywords(self.description)

        description_keywords -= name_keywords

        pairs = [
            (1.1, name_keywords),
            (0.5, description_keywords),
        ]

        q = Q()
        for importance, keywords in pairs:
            for keyword in keywords:
                q |= Q(
                    keyword=keyword,
                    importance__range=(importance - 0.05, importance + 0.05),
                )

        self.keyword_set.exclude(q).delete()

        current = set(self.keyword_set.values_list('keyword', flat=True))
        create = name_keywords.union(description_keywords) - current

        models = []
        for importance, keywords in pairs:
            models += [Keyword(
                recipe=self,
                keyword=keyword,
                importance=importance,
            ) for keyword in keywords.intersection(create)]

        Keyword.objects.bulk_create(models)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_index()


def recipe_image_upload_to(instance, filename):
    return 'recipes/{}/{}'.format(instance.id, filename)


class RecipeImage(TimeStampedModel):
    class Meta:
        ordering = ['main']

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=recipe_image_upload_to, blank=True)
    main = models.BooleanField(default=False)


class Step(TimeStampedModel):
    class Meta:
        ordering = ['sequence']
        unique_together = [['recipe', 'sequence']]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    sequence = models.IntegerField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Step {}'.format(self.sequence)


class Ingredient(TimeStampedModel):
    class Meta:
        ordering = ['created']

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    number = models.IntegerField()
    food = models.ForeignKey(Item, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return '{}{} {}'.format(self.number, self.unit if self.unit else '', self.food)


class Keyword(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=50)
    importance = models.FloatField()

    class Meta:
        indexes = [Index(fields=['keyword'])]
        constraints = [
            UniqueConstraint(fields=['keyword', 'recipe'], name='unique_keyword'),
        ]
