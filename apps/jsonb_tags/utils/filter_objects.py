from django.db.models import F, QuerySet

from apps.erm_tags.utils.filter_objects import FilterObjectsMeasure
from apps.jsonb_tags.models import TaggedInventory


class FilterJsonbObjectsMeasure(FilterObjectsMeasure):
    @staticmethod
    def get_queryset(name, value, value_filter_type) -> QuerySet:
        filter_condition = {
            f'tags__{name}{value_filter_type}': value
        }

        return (TaggedInventory.objects
            .filter(**filter_condition)
        )
