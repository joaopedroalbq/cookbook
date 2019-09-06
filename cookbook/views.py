from django.shortcuts import render

from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Recipe, Ingredient, FoodCategory

from .forms import RecipeForm


def index(request):
    # FoodCategory.objects.all().delete()
    # Ingredient.objects.all().delete()
    # Recipe.objects.all().delete()
    categories = FoodCategory.objects.all()
    ingredients = Ingredient.objects.all()
    recipes = Recipe.objects.all()
    # print(categories)
    # print(ingredients)
    # print(recipes)
    return render(request, 'cookbook/index.html', {'recipes': recipes})


def search(request):
    is_json = request.GET.get('json')
    search_parameter = request.GET.get('q')
    recipes = Recipe.objects.filter(name__icontains=search_parameter)
    ingredients = Ingredient.objects.filter(name__icontains=search_parameter)

    if is_json == 'true':
        html = render_to_string(
            template_name='cookbook/search_results_partial.html',
            context={'search_recipes': recipes, 'search_ingredients': ingredients}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    return render(request, 'cookbook/search_results.html', {'recipes': recipes, 'ingredients': ingredients})



# Recipes

class RecipeCreate(CreateView):
    form_class = RecipeForm
    template_name = 'cookbook/recipes/recipe_create.html'


class RecipeDelete(DeleteView):
    model = Recipe


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'cookbook/recipes/recipe_detail.html'


class RecipeList(ListView):
    model = Recipe
    template_name = 'cookbook/recipes/recipe_list.html'


class RecipeUpdate(UpdateView):
    form_class = RecipeForm
    template_name = 'cookbook/recipes/recipe_edit.html'

# Ingredients

class IngredientCreate(CreateView):
    model = Ingredient


class IngredientDelete(DeleteView):
    model = Ingredient


class IngredientDetail(DetailView):
    model = Ingredient
    template_name = 'cookbook/ingredients/ingredient_detail.html'

    def get(self, request, *args, **kwargs):
        is_json = request.GET.get('json')
        if is_json == 'true':
            ingredient = Ingredient.objects.get(id=self.kwargs['pk'])
            ingredient_data = {
                'id': ingredient.id,
                'name': ingredient.name,
                'unit': ingredient.unit,
                'amount': ingredient.amount,
                'cost': ingredient.cost
            }
            return JsonResponse(data=ingredient_data)
        return super(IngredientDetail, self).get(request, *args, **kwargs)


class IngredientList(ListView):
    model = Ingredient


class IngredientUpdate(UpdateView):
    model = Ingredient
