from django.core.management.base import BaseCommand, CommandError
from cookbook.models import FoodCategory, Ingredient, Recipe, RecipeIngredient

import random


class Command(BaseCommand):
    help = 'Feeds the database with some data'

    def handle(self, *args, **options):

        default_categories = [
            'Pizza',
            'Asian',
            'Burgers',
            'Barbecue',
            'Desserts',
            'Thai',
            'Sushi',
            'Others',
        ]

        for category in default_categories:
            try:
                c = FoodCategory(name=category)
                c.save()
            except Exception as e:
                raise CommandError('Error when trying to seed \n %s' % e.msg)

        default_ingredients = [
            {
                'name': 'Mozzarella Cheese',
                'article_number': '15O1A0351K',
                'unit': 'G',
                'amount': 500,
                'cost': 12,
            },
            {
                'name': 'Flour',
                'article_number': 'K1595SDF',
                'unit': 'KG',
                'amount': 1,
                'cost': 3,
            },
            {
                'name': 'Tomato',
                'article_number': 'G19D1HO',
                'unit': 'KG',
                'amount': 1,
                'cost': 7,
            },
            {
                'name': 'Basil',
                'article_number': 'OA91UIVD',
                'unit': 'G',
                'amount': 50,
                'cost': 0.4,
            },
        ]

        for ingredient in default_ingredients:
            try:
                i = Ingredient(
                    name=ingredient['name'],
                    article_number=ingredient['article_number'],
                    unit=ingredient['unit'],
                    amount=ingredient['amount'],
                    cost=ingredient['cost']
                )
                i.save()
            except Exception as e:
                raise CommandError('Error when trying to seed \n %s' % e.msg)

        default_recipe = {
                'name': 'Marguerita',
                'image': 'https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fcdn-image.myrecipes.com%2Fsites%2Fdefault%2Ffiles%2Fstyles%2Fmedium_2x%2Fpublic%2Fimage%2Frecipes%2Foh%2F12%2Fmozzarella-and-basil-pizza-oh-x.jpg%3Fitok%3D3jn_M-VX&w=450&c=sc&poi=face&q=85',
                'description': 'An easy pizza recipe with unbeatable flavor!',
                'instructions': 'This margherita pizza recipe begins with homemade pizza dough. Top with fresh mozzarella and tomatoes, then finish it off with garden-fresh basil.',
                'servings': 4,
                'difficulty': 1,
                'time': 2,
                'category': FoodCategory.objects.get(name='Pizza'),
            }

        try:
            r = Recipe(
                name=default_recipe['name'],
                image=default_recipe['image'],
                description=default_recipe['description'],
                instructions=default_recipe['instructions'],
                servings=default_recipe['servings'],
                difficulty=default_recipe['difficulty'],
                time=default_recipe['time'],
                category=default_recipe['category'],
            )
            r.save()
            ingredients = Ingredient.objects.all()
            for ingredient in ingredients:
                amount_used = 0
                if ingredient.unit == 'KG' or ingredient.unit == 'L':
                    amount_used = random.randint(1, 5)
                else:
                    amount_used = random.randint(100, 1000)
                ri = RecipeIngredient(ingredient=ingredient, recipe=r, amount_used=amount_used)
                ri.save()
        except Exception as e:
            raise CommandError('Error when trying to seed \n %s' % e.msg)

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded the database')
        )
