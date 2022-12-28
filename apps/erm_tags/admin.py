from django.contrib import admin

from apps.erm_tags.models import Tag, Inventory, InventoryTag


class InventoryTagInline(admin.TabularInline):
    raw_id_fields = ('tag', )

    model = InventoryTag
    extra = 1

class InventoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('type', )
    inlines = (InventoryTagInline, )


admin.site.register(Tag)
admin.site.register(Inventory, InventoryAdmin)
# admin.site.register(InventoryTag)
