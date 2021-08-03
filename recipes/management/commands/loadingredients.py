import json

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Создание моделей Игредиента по файлу "имя_файла.json"'

    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        if Ingredient.objects.exists():
            return

        filepath = options['filepath']
        with open(str(filepath), encoding='utf-8') as file:
            json_data = json.loads(file.read())
            for ingredient_data in json_data:
                Ingredient.objects.get_or_create(**ingredient_data)
