import grpc
import ingredient_pb2 as ingredient_pb2
import ingredient_pb2_grpc as ingredient_pb2_grpc


def run():
    # Connect to the gRPC server
    channel = grpc.insecure_channel('localhost:50051')
    stub = ingredient_pb2_grpc.IngredientServiceStub(channel)

    # Accept user input for ingredient details
    name = input("Enter ingredient name: ")
    quantity = float(input("Enter quantity: "))
    date_of_expiry = input("Enter expiry date (MM-DD-YYYY): ")

    # Create a request to add an ingredient
    ingredient_request = ingredient_pb2.IngredientRequest(
        name=name,
        quantity=quantity,
        date_of_expiry=date_of_expiry
    )

    # Call the AddIngredient RPC
    response = stub.AddIngredient(ingredient_request)
    print("Response received from server:", response.message)


if __name__ == '__main__':
    run()
