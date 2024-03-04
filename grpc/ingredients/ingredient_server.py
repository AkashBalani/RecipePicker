# server.py
from concurrent import futures
import grpc
# from recipe.views import IngredientService
import ingredient_pb2 as ingredient_pb2
import ingredient_pb2_grpc as ingredient_pb2_grpc
import requests
import logging

logging.basicConfig(level=logging.DEBUG)


class IngredientService(ingredient_pb2_grpc.IngredientServiceServicer):
    def AddIngredient(self, request, context):
        logging.info("AddIngredient Request Made:")
        logging.info("Ingredient: %s", request.name)
        logging.info("Quantity: %s", request.quantity)
        logging.info("Expiry Date: %s", request.date_of_expiry)

        data = {
            "name": request.name,
            "quantity": request.quantity,
            "date_of_expiry": request.date_of_expiry
        }

        try:
            response = requests.post(
                'http://localhost:8000/django/api/grpc/', json=data)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            logging.info("HTTP response status: %s", response.status_code)
            logging.info("HTTP response content: %s", response.text)
        except requests.exceptions.RequestException as e:
            logging.error("Error sending HTTP request: %s", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return ingredient_pb2.IngredientReply(message="Error adding ingredient")

        response = ingredient_pb2.IngredientReply()
        response.message = f"Ingredient {request.name} added successfully."
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ingredient_pb2_grpc._IngredientServiceServicer_to_serveradd(
        IngredientService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
