from django.urls import path
from .views import IngredientListCreateView

app_name = 'ingredients'

urlpatterns = [
    path('ingredients/', IngredientListCreateView.as_view(),
         name='ingredient-list-createv2'),
]
