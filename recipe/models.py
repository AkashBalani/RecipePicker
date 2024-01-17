from django.db import models
 
class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    date_of_expiry = models.DateField()

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title

