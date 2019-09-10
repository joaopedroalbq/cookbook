from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index_page'),
    path('search', views.search, name='search_view'),

    # Recipes
    path('recipes', views.RecipeList.as_view(), name='recipe_list'),
    path('recipes/category/<slug:category>', views.recipes_index_filter, name='recipes_index_filter'),
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

]
