import random

from django.db.models import F, QuerySet

from apps.commons.utils.get_queries_info import GetQueriesInfo
from apps.erm_tags.models import Tag, Inventory


class FilterObjectsMeasure(GetQueriesInfo):
    def __init__(self, value_filter_type='') -> None:
        self.value_filter_type = value_filter_type
        self.tags_values = self.get_tags_values()

    def get_tags_values(self) -> QuerySet:
        return (Tag.objects
            .filter(tag_inventories__isnull=False)
            .values('name', value=F('tag_inventories__value'))
        )
    
    @staticmethod
    def get_queryset(name, value, value_filter_type) -> QuerySet:
        filters_condition = {
            'tags__name': name,
            f'inventory_tags__value{value_filter_type}': value,
        }

        return (Inventory.objects
            .filter(**filters_condition)
        )

    def action(self) -> None:
        tags_values = self.tags_values
        value_filter_type = f'__{self.value_filter_type}' if self.value_filter_type else ''
        
        for tag_value in tags_values:
            name = tag_value['name']
            value = tag_value['value']

            if 'icontains' in value_filter_type or 'contains' in value_filter_type:
                indexes = sorted([
                    random.randint(0, len(value) - 1), random.randint(0, len(value) - 1)
                ])
                value = value[indexes[0]:indexes[1]]

            inventories = self.get_queryset(name, value, value_filter_type)

            if not inventories.all():
                raise Exception

            print(inventories.all())
