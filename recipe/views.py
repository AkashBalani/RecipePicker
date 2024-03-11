from django.shortcuts import render
from .models import Recipe, Ingredient
from rest_framework import generics as rest_generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_grpc_framework import mixins
from django_grpc_framework import generics as grpc_generics
from .serializers import IngredientSerializer, RecipeSerializer
from django.http import HttpResponseBadRequest, JsonResponse
import requests
import boto3
import logging
from django.views.decorators.http import require_GET
from django.conf import settings
from urllib.parse import quote
from prometheus_client import Counter, generate_latest, REGISTRY
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from kafka import KafkaConsumer
import json
import datetime
import pymysql
from .grpc.ingredients.ingredient_pb2 import IngredientRequest, IngredientReply

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Initialize SQS Client
sqs_client = boto3.client('sqs',
                          region_name='us-east-1',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                          )

# Requires QUEUE_URL to be set in settings.py
# Requires DATABASES to be set in settings.py
# Queues SQS messages and saves them to MySQL


class SQSPollingView(APIView):
    def get(self, request, *args, **kwargs):
        sqs_queue_url = settings.QUEUE_URL

        # Receive messages from the queue
        response = sqs_client.receive_message(
            QueueUrl=sqs_queue_url,
            MaxNumberOfMessages=1,  # Change this value as needed
            WaitTimeSeconds=20  # Change this value as needed
        )

        messages = response.get('Messages', [])
        if not messages:
            return Response({'message': 'No messages in the queue.'}, status=204)

        # Connect to MySQL
        connection = pymysql.connect(host=settings.DATABASES['default']['HOST'],
                                     user=settings.DATABASES['default']['USER'],
                                     password=settings.DATABASES['default']['PASSWORD'],
                                     database=settings.DATABASES['default']['NAME'])

        try:
            with connection.cursor() as cursor:
                # Process received messages
                for message in messages:
                    ingredient_data = json.loads(message['Body'])
                    # Process the ingredient_data as needed, for example, saving it to the database
                    date_str = ingredient_data.get('date_of_expiry', None)
                    if date_str:
                        try:
                            date_obj = datetime.datetime.strptime(
                                date_str, '%m-%d-%Y').date()
                            ingredient_data['date_of_expiry'] = date_obj
                        except ValueError:
                            logger.error(
                                f"Invalid date format: {date_str}. Skipping message.")
                            continue
                    else:
                        logger.error(
                            "Date field not found in message. Skipping message.")
                        continue

                    # Insert data into MySQL
                    sql = "INSERT INTO recipe_ingredient (name, quantity, date_of_expiry) VALUES (%s, %s, %s)"
                    cursor.execute(
                        sql, (ingredient_data['name'], ingredient_data['quantity'], ingredient_data['date_of_expiry']))
                    connection.commit()
                    logger.info("Inserted data into MySQL.")

                    # Delete the message from the queue
                    sqs_client.delete_message(
                        QueueUrl=sqs_queue_url,
                        ReceiptHandle=message['ReceiptHandle']
                    )
                    logger.info(
                        "Processed and deleted message from SQS queue.")

        finally:
            connection.close()

        return Response({'message': 'Messages processed successfully.'}, status=200)

# Requires QUEUE_URL to be set in settings.py
# Accepts POST requests with a list of ingredients and sends them to SQS


class IngredientListCreateView(rest_generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    def post(self, request, *args, **kwargs):
        # Assuming the SQS queue URL is stored in settings.py as SQS_QUEUE_URL
        sqs_queue_url = settings.QUEUE_URL

        # Assuming the request data is a list of ingredients
        ingredients = request.data.get('ingredients', [])
        if not ingredients:
            return Response({"error": "No ingredients provided in the request."}, status=400)

        # Send each ingredient to SQS queue
        for ingredient in ingredients:
            sqs_client.send_message(
                QueueUrl=sqs_queue_url,
                MessageBody=json.dumps(ingredient)
            )
        logger.info("Ingredients sent to SQS successfully.")
        return JsonResponse({'message': 'Ingredients sent to SQS successfully.'}, status=201)

# Accepts POST requests with a list of ingredients and saves them to MySQL


class IngredientListCreateView2(rest_generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response


class RecipeListCreateView(rest_generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)
        response['Access-Control-Allow-Origin'] = 'http://localhost:4200'
        response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

# Health and readiness checks


def health_check(request):
    return HttpResponse("Health Check - OK")


def ready_check(request):
    return HttpResponse("Readiness Check - OK")

# Accepts GET requests with params and returns a list of recipes


@csrf_protect
@require_GET
def find_recipes(request):
    logger = logging.getLogger(__name__)

    try:
        ingredients = request.GET.getlist('ingredient')
        excluded = request.GET.getlist('excluded')
        dietLabels = request.GET.getlist('dietLabels')
        mealType = request.GET.getlist('mealType')
        healthLabels = request.GET.getlist('healthLabels')
        cuisineType = request.GET.getlist('cuisineType')
        calcium = request.GET.get('calcium')

        params = {
            'type': 'public',
            'q': ','.join(ingredients),
            'app_id': settings.APP_ID,
            'app_key': settings.APP_KEY,
        }

        if ingredients:
            params['q'] = ','.join(ingredients)

        if excluded:
            params['excluded'] = ','.join(excluded)

        if dietLabels:
            params['diet'] = ','.join(dietLabels)

        if mealType:
            params['mealType'] = ','.join(mealType)

        if healthLabels:
            params['health'] = ','.join(healthLabels)

        if cuisineType:
            params['cuisineType'] = ','.join(cuisineType)

        if calcium:
            params['CA'] = calcium

        endpoint = 'https://api.edamam.com/api/recipes/v2'
        response = requests.get(endpoint, params=params)
        data = response.json()
        response_data = json.dumps(data)
        response = HttpResponse(response_data, content_type='application/json')
        return response

    except Exception as e:
        logger.exception("Error in find_recipes view: %s", str(e))
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)

# Expose the /metrics endpoint for Prometheus to scrape


def metrics_view(request):
    response = HttpResponse(generate_latest(REGISTRY))
    response['Content-Type'] = 'text/plain'
    return response

# Created a testing method for the gRPC server


class IngredientService(grpc_generics.GenericService):
    def AddIngredient(self, request, context):
        name = request.name
        quantity = request.quantity
        date_of_expiry = request.date_of_expiry
        print("Received Ingredient:")
        print("Name:", name)
        print("Quantity:", quantity)
        print("Date of Expiry:", date_of_expiry)
        return IngredientReply(message="Ingredient received successfully.")
