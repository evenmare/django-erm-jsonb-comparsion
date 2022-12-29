import csv

from django.core.management.base import BaseCommand, CommandError

from apps.erm_tags.utils.filter_objects import FilterObjectsMeasure
from apps.jsonb_tags.utils.filter_objects import FilterJsonbObjectsMeasure


class Command(BaseCommand):
    help = 'export stats to csv'

    def add_arguments(self, parser):
        parser.add_argument('type', type=str)
        parser.add_argument('value_filter', nargs='?', default=None)

    @staticmethod
    def get_class_by_measure_type(measure_type):
        if measure_type == 'erm':
            return FilterObjectsMeasure
        elif measure_type == 'jsonb':
            return FilterJsonbObjectsMeasure
        else:
            raise ValueError('type should be one of: erm, jsonb')
    
    @staticmethod
    def export(list_data, filename: str = 'export.csv'):
        fields = ['Number', 'Time']
        rows = [[i + 1, str(time).replace('.', ',')] for i, time in enumerate(list_data)]

        with open(filename, 'w') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(fields)
            writer.writerows(rows)

    def handle(self, *args, **options):
        measure_type = options['type']
        measure_class = self.get_class_by_measure_type(measure_type)
        
        value_filter = options.get('value_filter')

        operation = measure_class(value_filter)
        result = operation.execute()

        self.export(
            result,
            filename=f'{measure_type}{"__" + value_filter if value_filter else ""}.csv'
        )
