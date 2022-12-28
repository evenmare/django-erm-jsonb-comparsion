from rest_framework import serializers

from apps.jsonb_tags.models import TaggedInventory


class TaggedInventorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'type', 'tags', )
        model = TaggedInventory
