# server.py
from concurrent import futures
import grpc
# from recipe.views import IngredientService
import ingredient_pb2 as ingredient_pb2
import ingredient_pb2_grpc as ingredient_pb2_grpc


class IngredientService(ingredient_pb2_grpc.IngredientServiceServicer):
    def AddIngredient(self, request, context):
        print("AddIngredient Requst Made:")
        print("Ingredient:", request.name)
        print("Quantity:", request.quantity)
        print("Expiry Date:", request.date_of_expiry)

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
