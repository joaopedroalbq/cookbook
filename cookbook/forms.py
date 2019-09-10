from django.forms import ModelForm, ModelChoiceField, Select, CharField, IntegerField, TextInput, NumberInput

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


class IngredientForm(ModelForm):
    name = CharField(widget=TextInput(attrs={'class': 'p-2'}))
    article_number = CharField(widget=TextInput(attrs={'class': 'p-2'}))
    amount = IntegerField(widget=NumberInput(attrs={'class': 'p-2'}))
    cost = IntegerField(widget=NumberInput(attrs={'class': 'p-2'}))


    class Meta:
        model = Ingredient
        fields = (
            'name',
            'article_number',
            'unit',
            'amount',
            'cost',
        )
