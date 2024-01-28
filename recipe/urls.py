from django.urls import path
from .views import IngredientListCreateView, RecipeListCreateView, find_recipes, metrics_view, health_check, ready_check

app_name = 'recipes'

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view(),
         name='ingredient-list-create'),
    path('recipes/', RecipeListCreateView.as_view(), name='recipe-list-create'),
    path('find_recipes/', find_recipes, name='find_recipes'),
    path('metrics/', metrics_view, name='metrics'),
    path('health_check/', health_check, name='health_check'),
    path('ready_check/', ready_check, name='ready_check'),
]
