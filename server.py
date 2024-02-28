# server.py
from concurrent import futures
import grpc
from recipe.views import IngredientService
from django_grpc_framework.servers import grpc as django_grpc

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    django_grpc.add_servicer_to_server(IngredientService, server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
