import random

from django.apps import apps

from apps.commons.utils.generate_random import generate_random_string, generate_random_typed_value


TAGS_COUNT = 100
INVENTORY_COUNT = 150000
INVENTORY_TAGS_COUNT = 20


class ObjectCreation:
    @staticmethod
    def create_tags():
        data_types = ['str', 'int', 'float']

        tag_model = apps.get_model('erm_tags', 'Tag')
        tags = []

        for i in range(TAGS_COUNT):
            tags.append(
                tag_model(
                    name=generate_random_string(),
                    data_type=data_types[random.randint(0, 2)],
                )
            )

            print(f'tag instance {i + 1} / {TAGS_COUNT} created')
        
        tag_model.objects.bulk_create(tags)
        print('tags completed')
    
    @staticmethod
    def create_inventory():    
        types = list(apps.get_model('commons', 'Type').objects.all())

        inventory_model = apps.get_model('erm_tags', 'Inventory')
        inventories = []

        for i in range(INVENTORY_COUNT):
            inventories.append(inventory_model(
                name=generate_random_string(),
                type=types[random.randint(0, len(types) - 1)],
            ))
            print(f'inventory instance {i} / {INVENTORY_COUNT} created')

            if i % 1000 == 0:
                inventory_model.objects.bulk_create(inventories)
                inventories = []
            
        print('inventories completed')

    @staticmethod
    def create_inventory_tags():
        tags = list(apps.get_model('erm_tags', 'Tag').objects.all())

        inventory_model = apps.get_model('erm_tags', 'Inventory')
        inventory_tag_model = apps.get_model('erm_tags', 'InventoryTag')

        inventories = list(inventory_model.objects.all().order_by('-id'))
        inventories_tags = []
        
        for i, inventory in enumerate(inventories):
            allowed_tags = list(tags)

            for j in range(INVENTORY_TAGS_COUNT):
                tag = allowed_tags.pop(random.randint(0, len(allowed_tags) - 1))

                value = generate_random_typed_value(tag.data_type)
                
                inventories_tags.append(
                    inventory_tag_model(
                        tag=tag,
                        inventory=inventory,
                        value=value,
                    )
                )
            
            if i % 50 == 0:
                inventory_tag_model.objects.bulk_create(inventories_tags)
                inventories_tags = []
            
            print(f'inventory_tag instance {i * j} '
                    f'/ {INVENTORY_COUNT * INVENTORY_TAGS_COUNT} created'
            )
        
        print('inventory_tag completed')
