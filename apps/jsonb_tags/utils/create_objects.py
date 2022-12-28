import random

from django.apps import apps

from apps.commons.utils.generate_random import generate_random_string, generate_random_typed_value


TAGGED_INVENTORY_COUNT = 150000
TAGGED_INVENTORY_TAGS_COUNT = 20


def generate_jsonb_objects():
    types = list(apps.get_model('commons', 'Type').objects.all())
    tags = list(apps.get_model('erm_tags', 'Tag').objects.all())

    tagged_inventories_model = apps.get_model('jsonb_tags', 'TaggedInventory')
    tagged_inventories = []

    for i in range(TAGGED_INVENTORY_COUNT):
        tags_data = {}
        allowed_tags = list(tags)

        for j in range(TAGGED_INVENTORY_TAGS_COUNT):
            tag = allowed_tags.pop(random.randint(0, len(allowed_tags) - 1))
            value = generate_random_typed_value(tag.data_type)
            tags_data.update({tag.name: value})
        
        tagged_inventories.append(
            tagged_inventories_model(
                name=generate_random_string(),
                type=types[random.randint(0, len(types) - 1)],
                tags=tags_data,
            )
        )

        if i % 500 == 0:
            tagged_inventories_model.objects.bulk_create(tagged_inventories)
            tagged_inventories = []

        print(f'tagged inventory {i + 1} / {TAGGED_INVENTORY_COUNT} created')
