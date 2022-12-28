import random

from django.db.models import QuerySet

from apps.erm_tags.utils.filter_objects import FilterObjectsMeasure
from apps.erm_tags.models import Tag
from apps.jsonb_tags.models import TaggedInventory


class FilterJsonbObjectsMeasure(FilterObjectsMeasure):
    def get_tags_values(self) -> QuerySet:        
        tagged_inventories = (
            TaggedInventory.objects
                .values_list('tags', flat=True)[:self.TAGS_VALUES_COUNT]
        )

        if self.value_filter_type in ('contains', 'icontains'):
            raw_tagged_inventories = list(tagged_inventories)
            tagged_inventories = []

            for raw_tagged_inventory in raw_tagged_inventories:
                tagged_inventory = dict(raw_tagged_inventory)

                for key, value in raw_tagged_inventory.items():
                    if type(value) != str:
                        tagged_inventory.pop(key)
                
                tagged_inventories.append(tagged_inventory)

        tags_values = []

        for tagged_inventory in tagged_inventories:
            key = random.choice(list(tagged_inventory.keys()))
            tags_values.append(
                {
                    'name': key,
                    'value': tagged_inventory[key],
                }
            )
        
        return tags_values

    def get_queryset(self, name: str, value, value_filter_type: str) -> QuerySet:
        if self.value_filter_type in ('contains', 'icontains'):
            filter_condition = {
                f'tags{value_filter_type}': {name: value}
            }
        else:
            filter_condition = {
                f'tags__{name}{value_filter_type}': value
            }

        return (TaggedInventory.objects
            .filter(**filter_condition)
        )
