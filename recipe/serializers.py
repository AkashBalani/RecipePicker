from rest_framework import serializers
from .models import Ingredient, Recipe

class IngredientSerializer(serializers.ModelSerializer):

    date_of_expiry = serializers.DateField(format='%m-%d-%Y', input_formats=['%m-%d-%Y'])

    class Meta:
        model = Ingredient
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['date_of_expiry'] = instance.date_of_expiry.strftime('%m-%d-%Y')
        return representation
    
class RecipeSerializer(serializers.ModelSerializer):
    Ingredients = IngredientSerializer(many=True)
    
    class Meta:
        model = Recipe
        fields = '__all__'
