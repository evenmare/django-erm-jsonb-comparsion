from rest_framework.generics import ListAPIView

from apps.commons.filters import FieldsQueryFilter
from apps.erm_tags.models import Inventory
from apps.erm_tags.serializers import InventorySerializer


class ErmInventoryView(ListAPIView):
    queryset = Inventory.objects.exclude(tags=None)
    filter_backends = [FieldsQueryFilter, ]
    serializer_class = InventorySerializer
