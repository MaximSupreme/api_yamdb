import csv

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Import data from .csv file in db'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help='Full path to .csv file')
        parser.add_argument('--model_name', type=str, help='Model name')
        parser.add_argument('--app_name', type=str,
                            help='App name that uses the model')

    def handle(self, *args, **options):
        try:
            file_path = options.get('path')
            model = apps.get_model(options['app_name'], options['model_name'])
        except Exception:
            raise CommandError('Missing required keys. Use --help')
        with open(file=file_path) as file:
            reader = csv.reader(file)
            fields = next(reader)
            for row in reader:
                mapped_data = {
                    field: value for field, value in zip(fields, row)
                }
                obj = model.objects.get_or_create(**mapped_data)
                print(f'{model} {obj[0]} created')
