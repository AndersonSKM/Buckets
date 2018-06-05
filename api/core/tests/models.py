from django.db import models

from core.models import AbstractBaseModel, BaseModel

# Dummy models, just for testing


class Chef(BaseModel):
    name = models.CharField(max_length=20)


class Ingredient(AbstractBaseModel):
    name = models.CharField(max_length=10)


class Recipe(BaseModel):
    name = models.CharField(max_length=20)
    short_name = models.CharField(max_length=10)
    picture = models.ImageField()
    chef = models.ForeignKey(Chef, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipe')
    vegan = models.BooleanField(default=True)
    country = models.CharField(max_length=20, null=True, blank=True)
    time_to_cook = models.TimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateField(auto_now=True)
    pounds = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
