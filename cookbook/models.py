from django.db import models

from functools import reduce


class FoodCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    GRAM = 'G'
    KILOGRAM = 'KG'
    MILILITER = 'ML'
    LITER = 'L'
    UNIT_CHOICES = [
        (GRAM, 'g'),
        (KILOGRAM, 'Kg'),
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

    def __str__(self):
        return self.name


class Recipe(models.Model):
    ZERO_TWENTY_FIVE = 1
    THIRTY_FIFTY = 2
    ONE_HOUR_PLUS = 3
    TIME_CHOICES = [
        (ZERO_TWENTY_FIVE, '0-25 min'),
        (THIRTY_FIFTY, '30-50 min'),
        (ONE_HOUR_PLUS, '1 hour +'),
    ]
    EASY = 1
    MEDIUM = 2
    HARD = 3
    EXPERT = 4
    DIFFICULTY_CHOICES = [
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
        (EXPERT, 'Expert'),
    ]
    name = models.CharField(max_length=100)
    image = models.URLField(max_length=300)
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    category = models.ForeignKey(
        FoodCategory,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient'
    )
    time = models.IntegerField(
        choices=TIME_CHOICES,
        default=ZERO_TWENTY_FIVE
    )

    def __str__(self):
        return self.name

    def get_time(self):
        return self.TIME_CHOICES[self.time][1]
    
    def get_overral_cost(self):
        ingredients_used = RecipeIngredient.objects.all()
        return sum([i.get_cost() for i in ingredients_used], 0)


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount_used = models.IntegerField()

    def get_cost(self):
        return (self.amount_used * self.ingredient.cost) / self.ingredient.amount
