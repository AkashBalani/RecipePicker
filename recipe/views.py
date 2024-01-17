from django.shortcuts import render
from .models import Recipe, Ingredient
from rest_framework import generics
from .serializers import IngredientSerializer, RecipeSerializer
from django.http import JsonResponse
import requests
import logging
from django.views.decorators.http import require_GET
from django.conf import settings

class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

@require_GET
def find_recipes(request):
    logger = logging.getLogger(__name__)

    try:

      ingredients = request.GET.getlist('ingredient')

      if not ingredients:
          return JsonResponse({'error': 'Please provide at least one ingredient'}, status=400)

      endpoint = 'https://api.edamam.com/search'

      params = {
          'q': ','.join(ingredients),
          'app_id': settings.APP_ID,
          'app_key': settings.APP_KEY,
      }

      response = requests.get(endpoint, params=params)

      data = response.json()
      return JsonResponse(data)
    except Exception as e:
        logger.exception("Error in find_recipes view: %s", str(e))

        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)