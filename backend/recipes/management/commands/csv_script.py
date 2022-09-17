import csv

from django.core.management import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Creating Ingredients objects from csv file')
        with open('./data/ingredients.csv', encoding='utf-8') as file_obj:
            csv_obj = csv.reader(file_obj, delimiter=',')
            for row in csv_obj:
                Ingredient.objects.create(
                    name=row[0], measurement_unit=row[1])
