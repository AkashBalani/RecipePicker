# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: recipe.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0crecipe.proto\x12\x06recipe\"\x9c\x01\n\rRecipeRequest\x12\x13\n\x0bingredients\x18\x01 \x03(\t\x12\x10\n\x08\x65xcluded\x18\x02 \x03(\t\x12\x13\n\x0b\x64iet_labels\x18\x03 \x03(\t\x12\x11\n\tmeal_type\x18\x04 \x03(\t\x12\x15\n\rhealth_labels\x18\x05 \x03(\t\x12\x14\n\x0c\x63uisine_type\x18\x06 \x03(\t\x12\x0f\n\x07\x63\x61lcium\x18\x07 \x01(\t\"\x99\x01\n\x0eRecipeResponse\x12-\n\x06recipe\x18\x01 \x03(\x0b\x32\x1d.recipe.RecipeResponse.Recipe\x1aX\n\x06Recipe\x12\r\n\x05label\x18\x01 \x01(\t\x12\r\n\x05image\x18\x02 \x01(\t\x12\x13\n\x0bingredients\x18\x03 \x03(\t\x12\x0b\n\x03url\x18\x04 \x01(\t\x12\x0e\n\x06source\x18\x05 \x01(\t2M\n\rRecipeService\x12<\n\x0b\x46indRecipes\x12\x15.recipe.RecipeRequest\x1a\x16.recipe.RecipeResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'recipe_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_RECIPEREQUEST']._serialized_start=25
  _globals['_RECIPEREQUEST']._serialized_end=181
  _globals['_RECIPERESPONSE']._serialized_start=184
  _globals['_RECIPERESPONSE']._serialized_end=337
  _globals['_RECIPERESPONSE_RECIPE']._serialized_start=249
  _globals['_RECIPERESPONSE_RECIPE']._serialized_end=337
  _globals['_RECIPESERVICE']._serialized_start=339
  _globals['_RECIPESERVICE']._serialized_end=416
# @@protoc_insertion_point(module_scope)