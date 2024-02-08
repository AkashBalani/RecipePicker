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

        # print(f'Raw calcium value: {calcium}')

        if calcium:
            calcium = calcium.strip()  # Remove leading and trailing whitespaces

        # print(f'Before encoding: {calcium}')

        # calcium = quote(calcium, safe='')

        # print(f'After encoding: {calcium}')

        if not ingredients:
            return JsonResponse({'error': 'Please provide at least one ingredient'}, status=400)

        endpoint = 'https://api.edamam.com/search'

        if excluded and dietLabels:
            params = {
                'q': ','.join(ingredients),
                'excluded': ','.join(excluded),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
            }

        if excluded:
            params = {
                'q': ','.join(ingredients),
                'excluded': ','.join(excluded),
                # 'CA': calcium if isinstance(calcium, str) else ','.join(calcium),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
            }
            print(params)

        if dietLabels:
            params = {
                'q': ','.join(ingredients),
                'diet': ','.join(dietLabels),
                'app_id': settings.APP_ID,
                'app_key': settings.APP_KEY,
            }

        else:
            params = {
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
