from django.shortcuts import render

from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import Recipe, Ingredient, FoodCategory

from .forms import RecipeForm


def index(request):
    # FoodCategory.objects.all().delete()
    # Ingredient.objects.all().delete()
    # Recipe.objects.all().delete()
    categories = FoodCategory.objects.all()
    ingredients = Ingredient.objects.all()
    recipes = Recipe.objects.all()
    print(categories)
    print(ingredients)
    print(recipes)
    return render(request, 'cookbook/index.html', {'recipes': recipes})


# Recipes

class RecipeCreate(CreateView):
    form_class = RecipeForm
    template_name = 'cookbook/recipes/recipe_form.html'


class RecipeDelete(DeleteView):
    model = Recipe


class RecipeDetail(DetailView):
    model = Recipe


class RecipeList(ListView):
    model = Recipe
    template_name = 'cookbook/recipes/recipe_list.html'


class RecipeUpdate(UpdateView):
    model = Recipe


# Ingredients

class IngredientCreate(CreateView):
    model = Ingredient


class IngredientDelete(DeleteView):
    model = Ingredient


class IngredientDetail(DetailView):
    model = Ingredient


class IngredientList(ListView):
    model = Ingredient


class IngredientUpdate(UpdateView):
    model = Ingredient


# Categories


class CategoryCreate(CreateView):
    model = FoodCategory


class CategoryDelete(DeleteView):
    model = FoodCategory


class CategoryDetail(DetailView):
    model = FoodCategory


class CategoryList(ListView):
    model = FoodCategory


class CategoryUpdate(UpdateView):
    model = FoodCategory
