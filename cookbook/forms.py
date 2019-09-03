from django.forms import ModelForm

from .models import Recipe, Ingredient, FoodCategory


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'rating',
            'category',
            'ingredients',
            'time_from',
            'time_to'
        )
