from django.db import models


class FoodCategory(models.Model):
    name = models.CharField(max_length=100)


class Ingredient(models.Model):
    GRAM = 'G'
    KILOGRAM = 'KG'
    CENTILITER = 'CL'
    MILILITER = 'ML'
    LITER = 'L'
    UNIT_CHOICES = [
        (GRAM, 'g'),
        (KILOGRAM, 'Kg'),
        (CENTILITER, 'cL'),
        (MILILITER, 'mL'),
        (LITER, 'L'),
    ]
    name = models.CharField(max_length=100)
    article_number = models.CharField(max_length=64)
    unit = models.CharField(
        max_length=2,
        choices=UNIT_CHOICES,
        default=KILOGRAM
    )
    amount = models.IntegerField()
    cost = models.FloatField()


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=300)
    rating = models.FloatField()
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    ingredients = models.ManyToManyField(Ingredient)
    time_from = models.SmallIntegerField()
    time_to = models.SmallIntegerField()
