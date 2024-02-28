# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import ingredient_pb2 as ingredient__pb2


class IngredientServiceStub(object):
    """Ingredient service definition.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddIngredient = channel.unary_unary(
                '/ingredient.IngredientService/AddIngredient',
                request_serializer=ingredient__pb2.IngredientRequest.SerializeToString,
                response_deserializer=ingredient__pb2.IngredientReply.FromString,
                )


class IngredientServiceServicer(object):
    """Ingredient service definition.
    """

    def AddIngredient(self, request, context):
        """Unary
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IngredientServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddIngredient': grpc.unary_unary_rpc_method_handler(
                    servicer.AddIngredient,
                    request_deserializer=ingredient__pb2.IngredientRequest.FromString,
                    response_serializer=ingredient__pb2.IngredientReply.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ingredient.IngredientService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IngredientService(object):
    """Ingredient service definition.
    """

    @staticmethod
    def AddIngredient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/ingredient.IngredientService/AddIngredient',
            ingredient__pb2.IngredientRequest.SerializeToString,
            ingredient__pb2.IngredientReply.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)