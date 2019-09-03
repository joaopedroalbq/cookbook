from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index_page'),


    # Recipes
    path('recipes', views.RecipeList.as_view(), name='recipe_list'),
    path('recipes/<int:pk>', views.RecipeDetail.as_view(), name='recipe_details'),
    path('recipes/create', views.RecipeCreate.as_view(), name='recipe_create'),
    path('recipes/<int:pk>/update', views.RecipeUpdate.as_view(), name='recipe_update'),
    path('recipes/<int:pk>/delete', views.RecipeDelete.as_view(), name='recipe_delete'),

    # Ingredients
    path('ingredients', views.IngredientList.as_view(), name='ingredient_list'),
    path('ingredients/<int:pk>', views.IngredientDetail.as_view(), name='ingredient_details'),
    path('ingredients/create', views.IngredientCreate.as_view(), name='ingredient_create'),
    path('ingredients/<int:pk>/update', views.IngredientUpdate.as_view(), name='ingredient_update'),
    path('ingredients/<int:pk>/delete', views.IngredientDelete.as_view(), name='ingredient_delete'),

    # Categories
    path('categories', views.CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>', views.CategoryDetail.as_view(), name='category_details'),
    path('categories/create', views.CategoryCreate.as_view(), name='category_create'),
    path('categories/<int:pk>/update', views.CategoryUpdate.as_view(), name='category_update'),
    path('categories/<int:pk>/delete', views.CategoryDelete.as_view(), name='category_delete'),
]
