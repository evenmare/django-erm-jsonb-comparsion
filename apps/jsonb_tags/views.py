from rest_framework.generics import ListAPIView

from apps.commons.filters import FieldsQueryFilter
from apps.jsonb_tags.models import TaggedInventory
from apps.jsonb_tags.serializers import TaggedInventorySerializer


class JsonbInventoryView(ListAPIView):
    queryset = TaggedInventory.objects.exclude(tags=None)
    filter_backends = [FieldsQueryFilter, ]
    serializer_class = TaggedInventorySerializer