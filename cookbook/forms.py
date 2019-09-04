from django.forms import ModelForm, ModelChoiceField, Select

from .models import Recipe, Ingredient, FoodCategory


class RecipeForm(ModelForm):

    ingredients = ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=Select(
            attrs={
                'class': 'block appearance-none w-full py-3 px-4 pr-8 rounded bg-white',
                'v-model': 'selectedIngredient',
                '@change': 'addIngredient'
            }
        )
    )

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
