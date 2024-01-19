from django.shortcuts import render
from .models import Ingredient
from rest_framework import generics
from .serializers import IngredientSerializer


class IngredientListCreateView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
