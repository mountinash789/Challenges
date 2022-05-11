from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from cookbook.forms import TagForm
from cookbook.models import Tag, Item, Unit, Ingredient, Recipe, RecipeImage, Step


class IngredientInline(admin.TabularInline):
    model = Ingredient
    autocomplete_fields = ['food', 'unit']
    extra = 0


class StepInline(admin.TabularInline):
    model = Step
    extra = 0


class RecipeImageInline(admin.TabularInline):
    model = RecipeImage
    extra = 0


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [
        IngredientInline,
        StepInline,
        RecipeImageInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    form = TagForm
    list_display = ['description']
    search_fields = ['description']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description']

    def clean(self):
        if Item.objects.filter(description__iexact=self.cleaned_data['description']).exists():
            raise ValidationError(
                message="Item with this Description already exists.",
            )
        super().clean()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['description']
    search_fields = ['description']
    form = ItemForm


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['description']
    search_fields = ['description']
