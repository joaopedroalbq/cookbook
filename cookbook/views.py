from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.db.models import Q, Count

from .models import Recipe, Ingredient, FoodCategory, RecipeIngredient

from .forms import RecipeForm

import json


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
    model = Recipe
    success_url = reverse_lazy('index_page')

    def post(self, request):
        form_data = json.loads(request.body)
        category = FoodCategory.objects.get(name=form_data['category'])
        new_recipe = Recipe(
            name=form_data['name'],
            image=form_data['image'],
            description=form_data['description'],
            servings=form_data['servings'],
            category=category,
            time=form_data['time'],
            instructions=form_data['instructions'],
            difficulty=form_data['difficulty']
        )
        new_recipe.save()
        for ingredient in form_data['ingredients']:
            used_ingredient = Ingredient.objects.get(id=ingredient['id'])
            ri = RecipeIngredient(
                recipe=new_recipe,
                ingredient=used_ingredient,
                amount_used=ingredient['amount_used']
            )
            ri.save()
        return redirect(new_recipe)


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('index_page')


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'cookbook/recipes/recipe_detail.html'


class RecipeList(ListView):
    model = Recipe
    template_name = 'cookbook/recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 6


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_count = {category.name:0 for category in FoodCategory.objects.all()}
        recipes = Recipe.objects.filter(ingredients=super().get_object())
        for recipe in recipes:
            categories_count[recipe.category.name] += 1
        context['categories_count'] = categories_count
        context['times_used'] = recipes.count()
        context['recipes'] = recipes[:3]
        return context

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
    template_name = 'cookbook/ingredients/ingredient_list.html'
    context_object_name = 'ingredients'
    paginate_by = 20

class IngredientUpdate(UpdateView):
    model = Ingredient
