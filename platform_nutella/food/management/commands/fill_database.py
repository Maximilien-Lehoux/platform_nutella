from django.core.management.base import BaseCommand
from food.models import Food, FoodSubstitute
from food.api_openfoodfact import DataApi
from django.db.utils import IntegrityError
import requests
from django.db import transaction

foods_choose = ["nutella", "pâte", "cassoulet", "confiture", "prince",
               "yaourt", "soda"]


class Command(BaseCommand):
    help = 'Fill the database with OpenFoodFacts data'

    def handle(self, *args, **options):
        self.stdout.write('La base de données se remplie...')
        Food.objects.all().delete()

        for food_choose in foods_choose:
            data_api_openfoodfact = DataApi(food_choose)
            data_products_category = data_api_openfoodfact.select_key_test()

            name_food_nutriscore = \
                data_api_openfoodfact.get_nutriscore_food_choose()
            name_food_category = \
                data_api_openfoodfact.get_categories_name_food()

            name_food = Food(name=food_choose,
                             nutriscore=name_food_nutriscore,
                             category=name_food_category)

            name_food.save()

            for data_product_category in data_products_category:
                name = (data_product_category[0])
                image = (data_product_category[1])
                nutriscore = (data_product_category[2])
                url = (data_product_category[3])
                fat = (data_product_category[4])
                fat_saturated = (data_product_category[5])
                sugar = (data_product_category[6])
                salt = (data_product_category[7])

                food_substitutes = FoodSubstitute(name=name,
                                                  image=image,
                                                  nutriscore=nutriscore,
                                                  url=url,
                                                  food_id=name_food.pk,
                                                  nutriments_fat=fat,
                                                  nutriments_fat_saturated=fat_saturated,
                                                  nutriments_salt=salt,
                                                  nutriments_sugars=sugar)
                food_substitutes.save()

        self.stdout.write('Base de données remplie avec succès')


