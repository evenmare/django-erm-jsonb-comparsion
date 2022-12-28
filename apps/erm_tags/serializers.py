from rest_framework import serializers

from apps.erm_tags.models import Inventory, InventoryTag


def get_value(data_type: str, raw_value):
    if data_type == 'int':
        return int(raw_value)
    elif data_type == 'float':
        return float(raw_value)
    else:
        return raw_value


# class InventoryTagSerializer(serializers.ModelSerializer):
#     id = serializers.ReadOnlyField(source='tag.id')
#     name = serializers.ReadOnlyField(source='tag.name')
#     value = serializers.SerializerMethodField()

#     def get_value(self, obj: InventoryTag):
#         raw_value = obj.value
#         data_type = obj.tag.data_type

#         return get_value(data_type, raw_value)

#     class Meta:
#         fields = ('id', 'name', 'value', )
#         model = InventoryTag


class InventorySerializer(serializers.ModelSerializer):
    # tags = InventoryTagSerializer(source='inventory_tags', many=True)
    tags = serializers.SerializerMethodField()

    def get_tags(self, obj: Inventory):
        inventory_tags = InventoryTag.objects.filter(inventory=obj)
        tags_data = {
            inventory_tag.tag.name: get_value(inventory_tag.tag.data_type, inventory_tag.value)
            for inventory_tag in inventory_tags
        }
        return tags_data

    class Meta:
        fields = ('id', 'name', 'type', 'tags', )
        model = Inventory
