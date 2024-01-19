from django.urls import path
from .views import IngredientListCreateView, RecipeListCreateView, find_recipes

app_name = 'recipes'

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view(),
         name='ingredient-list-create'),
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('find_recipes/', find_recipes, name='find_recipes'),
]
