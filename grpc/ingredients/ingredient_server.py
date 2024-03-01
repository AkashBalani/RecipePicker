# server.py
from concurrent import futures
import grpc
# from recipe.views import IngredientService
import ingredient_pb2 as ingredient_pb2
import ingredient_pb2_grpc as ingredient_pb2_grpc
import requests


class IngredientService(ingredient_pb2_grpc.IngredientServiceServicer):
    def AddIngredient(self, request, context):
        print("AddIngredient Requst Made:")
        print("Ingredient:", request.name)
        print("Quantity:", request.quantity)
        print("Expiry Date:", request.date_of_expiry)

        data = {
            "name": request.name,
            "quantity": request.quantity,
            "date_of_expiry": request.date_of_expiry
        }

        try:
            response = requests.post(
                'http://localhost:8000/django/api/ingredients', json=data)
            response.raise_for_status()  # Raise an exception for non-2xx responses
            print("HTTP response status:", response.status_code)
            print("HTTP response content:", response.text)
        except requests.exceptions.RequestException as e:
            print("Error sending HTTP request:", e)

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
