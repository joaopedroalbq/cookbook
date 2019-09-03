from django.core.management.base import BaseCommand, CommandError
from cookbook.models import FoodCategory, Ingredient, Recipe


class Command(BaseCommand):
    help = 'Feeds the database with default values'

    def handle(self, *args, **options):

        default_categories = [
            'Pizza',
            'Asian',
            'Burgers',
            'Barbecue',
            'Desserts',
            'Thai',
            'Sushi',
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
                'cost': 12
            },
            {
                'name': 'Flour',
                'article_number': 'K1595SDF',
                'unit': 'KG',
                'amount': 1,
                'cost': 3
            },
            {
                'name': 'Tomato',
                'article_number': 'G19D1HO',
                'unit': 'KG',
                'amount': 1,
                'cost': 7
            },
            {
                'name': 'Basil',
                'article_number': 'OA91UIVD',
                'unit': 'G',
                'amount': 50,
                'cost': 0.4
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

        default_recipes = [
            {
                'name': 'Marguerita',
                'image': 'https://imagesvc.meredithcorp.io/v3/mm/image?url=https%3A%2F%2Fcdn-image.myrecipes.com%2Fsites%2Fdefault%2Ffiles%2Fstyles%2Fmedium_2x%2Fpublic%2Fimage%2Frecipes%2Foh%2F12%2Fmozzarella-and-basil-pizza-oh-x.jpg%3Fitok%3D3jn_M-VX&w=450&c=sc&poi=face&q=85',
                'rating': 4.7,
                'time_from': 30,
                'time_to': 45,
                'category': FoodCategory.objects.get(name='Pizza')
            },
        ]

        # TODO: Add more default recipes
        # As the intended use of the seed function is to get going
        # with some simple data, this section of the code runs
        # through the previously added ingredients.
        for recipe in default_recipes:
            try:
                r = Recipe(
                    name=recipe['name'],
                    image=recipe['image'],
                    rating=recipe['rating'],
                    time_from=recipe['time_from'],
                    time_to=recipe['time_to'],
                )
                r.save()
                ingredients = Ingredient.objects.all()
                for ingredient in ingredients:
                    r.ingredients.add(ingredient)
                r.category = recipe['category']
                r.save()
            except Exception as e:
                raise CommandError('Error when trying to seed \n %s' % e.msg)

        self.stdout.write(
            self.style.SUCCESS('Successfully seeded the database')
        )
