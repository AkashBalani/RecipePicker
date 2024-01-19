from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    date_of_expiry = models.DateField()
