from django.shortcuts import render, redirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Recipe, Ingredient, FoodCategory, RecipeIngredient

from .forms import RecipeForm, IngredientForm

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
    ingredients = Ingredient.objects.filter(
        Q(name__icontains=search_parameter) | Q(article_number__icontains=search_parameter)
    )

    if is_json == 'true':
        html = render_to_string(
            template_name='cookbook/search_results_partial.html',
            context={'search_recipes': recipes, 'search_ingredients': ingredients}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict)

    return render(
                request,
                'cookbook/search_results.html',
                {
                    'recipes': recipes,
                    'ingredients': ingredients
                }
            )


# Recipes

def recipes_index_filter(request, *args, **kwargs):
    search_parameter = kwargs['category']
    if search_parameter == 'All':
        category = FoodCategory.objects.all()
    else:
        category = [FoodCategory.objects.get(name=search_parameter)]
    recipes = []
    for recipe in Recipe.objects.filter(category__in=category):
        recipes.append(
            {
                'id': recipe.id,
                'name': recipe.name,
                'time': recipe.get_time(),
                'difficulty': recipe.difficulty,
                'category': recipe.category.name,
                'cost': recipe.get_overral_cost(),
                'image': recipe.image,
            }
        )
    return JsonResponse(data={'recipes': recipes})


class RecipeCreate(CreateView):
    form_class = RecipeForm
    template_name = 'cookbook/recipes/recipe_create.html'
    model = Recipe
    success_url = reverse_lazy('recipe_list')

    def post(self, request):
        form_data = json.loads(request.body)
        category = FoodCategory.objects.get(name=form_data['category'])
        if form_data['name'] == '':
            return JsonResponse(
                {
                    'message': 'You must provide a name for the recipe',
                    'status': 400
                }
            )
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
        return JsonResponse(
                {
                    'message': 'Success!',
                    'new_recipe_id': new_recipe.id,
                    'status': 200
                }
            )


class RecipeDelete(DeleteView):
    model = Recipe
    success_url = reverse_lazy('recipe_list')


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'cookbook/recipes/recipe_detail.html'


class RecipeList(ListView):
    model = Recipe
    template_name = 'cookbook/recipes/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 6


class RecipeUpdate(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'cookbook/recipes/recipe_edit.html'

    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body)
        category = FoodCategory.objects.get(name=form_data['category'])
        recipe = Recipe.objects.get(id=form_data['id'])
        recipe.name = form_data['name']
        if recipe.name == '':
            return JsonResponse(
                {
                    'message': 'You must provide a name for the recipe',
                    'status': 400
                }
            )
        recipe.image = form_data['image']
        recipe.description = form_data['description']
        recipe.servings = form_data['servings']
        recipe.category = category
        recipe.time = form_data['time']
        recipe.instructions = form_data['instructions']
        recipe.difficulty = form_data['difficulty']
        recipe.save()
        for ingredient in form_data['ingredients']:
            used_ingredient = Ingredient.objects.get(id=ingredient['id'])
            ri = RecipeIngredient.objects.get(
                recipe=recipe,
                ingredient=used_ingredient,
            )
            ri.amount_used = ingredient['amount_used']
            ri.save()
        return JsonResponse(
                {
                    'message': 'Success!',
                    'status': 200
                }
            )


# Ingredients

class IngredientCreate(CreateView):
    model = Ingredient
    success_url = reverse_lazy('ingredient_list')
    form_class = IngredientForm
    template_name = 'cookbook/ingredients/ingredient_form.html'
    extra_context = {'action': 'Create', 'previous_page': 'ingredient_list'}



class IngredientDelete(DeleteView):
    model = Ingredient
    success_url = reverse_lazy('ingredient_list')
    


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
    success_url = reverse_lazy('ingredient_list')
    form_class = IngredientForm
    template_name = 'cookbook/ingredients/ingredient_form.html'
    extra_context = {'action': 'Edit', 'previous_page': 'ingredient_details'}
