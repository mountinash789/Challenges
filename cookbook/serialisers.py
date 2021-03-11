from rest_framework import serializers

from cookbook.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    cooking_time_format = serializers.CharField(read_only=True)
    tags_display = serializers.CharField(source='get_tags_display', read_only=True)

    class Meta:
        model = Recipe
        fields = [
            "id",
            "name",
            "description",
            "cooking_time_format",
            "tags_display",
        ]
