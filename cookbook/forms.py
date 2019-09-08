from django.forms import ModelForm, ModelChoiceField, Select

from .models import Recipe, Ingredient, FoodCategory


class RecipeForm(ModelForm):

    ingredients = ModelChoiceField(
        queryset=Ingredient.objects.all(),
        widget=Select(
            attrs={
                'class': 'block appearance-none w-full py-3 px-4 pr-8 rounded bg-white',
                'v-model': 'selectedIngredient'
            }
        )
    )

    class Meta:
        model = Recipe
        fields = (
            'name',
            'image',
            'description',
            'category',
            'ingredients',
            'instructions',
            'difficulty',
            'time',
        )
