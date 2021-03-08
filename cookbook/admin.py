from django.contrib import admin

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


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['description']
    search_fields = ['description']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['description']
    search_fields = ['description']
