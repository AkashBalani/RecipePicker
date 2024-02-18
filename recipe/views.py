from django.shortcuts import render
from .models import Recipe, Ingredient
from rest_framework import generics
from .serializers import IngredientSerializer, RecipeSerializer
from django.http import JsonResponse
import requests
import logging
from django.views.decorators.http import require_GET
from django.conf import settings
from urllib.parse import quote
from prometheus_client import Counter, generate_latest, REGISTRY
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from kafka import KafkaConsumer
import json

# # Initialize Kafka Consumer
# consumer = KafkaConsumer('test',
#                          bootstrap_servers=['127.0.0.1:9093'],
#                          auto_offset_reset='earliest',
#                          enable_auto_commit=True,
#                          value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# for message in consumer:
#     print("Received message:", message.value)

logger = logging.getLogger(__name__)


class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = 'http://localhost:4200'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


class RecipeListCreateView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = 'http://localhost:4200'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


def health_check(request):
    return HttpResponse("OK")


def ready_check(request):
    return HttpResponse("OK")


@csrf_protect
@require_GET
def find_recipes(request):
    logger = logging.getLogger(__name__)

    try:

        ingredients = request.GET.getlist('ingredient')

        excluded = request.GET.getlist('excluded')

        calcium = request.GET.get('calcium')

        dietLabels = request.GET.getlist('dietLabels')

        mealType = request.GET.getlist('mealType')

        healthLabels = request.GET.getlist('healthLabels')

        if not ingredients:
            return JsonResponse({'error': 'Please provide at least one ingredient'}, status=400)

        endpoint = 'https://api.edamam.com/api/recipes/v2'

        if ingredients and excluded and dietLabels and mealType and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'mealType': ','.join(mealType),
                'health': ','.join(healthLabels),
            }

        if ingredients and excluded and dietLabels and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'health': ','.join(healthLabels),
            }

        if ingredients and excluded and healthLabels and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'mealType': ','.join(mealType),
                'health': ','.join(healthLabels),
            }

        if ingredients and healthLabels and dietLabels and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'mealType': ','.join(mealType),
                'health': ','.join(healthLabels),
            }

        if ingredients and excluded and dietLabels and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'mealType': ','.join(mealType),
            }

        if ingredients and dietLabels and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'mealType': ','.join(mealType),
            }

        if ingredients and excluded and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'mealType': ','.join(mealType),
            }

        if ingredients and dietLabels and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'health': ','.join(healthLabels),
            }

        if ingredients and healthLabels and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'mealType': ','.join(mealType),
                'health': ','.join(healthLabels),
            }

        if excluded and dietLabels and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'mealType': ','.join(mealType),
            }

        if excluded and dietLabels and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'health': ','.join(healthLabels),
            }

        if excluded and healthLabels and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'mealType': ','.join(mealType),
                'health': ','.join(healthLabels),
            }

        if ingredients and excluded and dietLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
            }

        if ingredients and excluded and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'mealType': ','.join(mealType),
            }

        if ingredients and excluded and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'health': ','.join(healthLabels),
            }

        if ingredients and dietLabels and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'mealType': ','.join(mealType),
            }

        if ingredients and dietLabels and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'health': ','.join(healthLabels),
            }

        if ingredients and mealType and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'mealType': ','.join(mealType),
                'health': ','.join(healthLabels),
            }

        if ingredients and excluded:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                # 'CA': calcium if isinstance(calcium, str) else ','.join(calcium),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
            }

        if ingredients and dietLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
            }

        if ingredients and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'mealType': ','.join(mealType),
            }

        if ingredients and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'health': ','.join(healthLabels),
            }

        if excluded and dietLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
            }

        if excluded and mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'mealType': ','.join(mealType),
            }

        if excluded and healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
                'health': ','.join(healthLabels),
            }

        if excluded:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                # 'CA': calcium if isinstance(calcium, str) else ','.join(calcium),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'excluded': ','.join(excluded),
            }
            print(params)

        if dietLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
            }

        if mealType:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'mealType': ','.join(mealType),
            }

        if healthLabels:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'health': ','.join(healthLabels),
            }

        if calcium:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
                'CA': calcium,
            }

        else:
            params = {
                'type': 'public',
                'q': ','.join(ingredients),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
            }

        response = requests.get(endpoint, params=params)

        data = response.json()
        return JsonResponse(data, safe=False)
    except Exception as e:
        logger.exception("Error in find_recipes view: %s", str(e))

        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)


requests_counter = Counter('django_http_requests_total', 'Total HTTP Requests')


def some_view(request):
    # Increment the counter metric on each request
    requests_counter.inc()
    # Your view logic here
    return HttpResponse("Hello, world!")


def metrics_view(request):
    # Expose the /metrics endpoint for Prometheus to scrape
    response = HttpResponse(generate_latest(REGISTRY))
    response['Content-Type'] = 'text/plain'
    return response
