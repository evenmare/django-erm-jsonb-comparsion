from django.contrib import admin
from django.db import models

from django_json_widget.widgets import JSONEditorWidget

from apps.jsonb_tags.models import TaggedInventory


class TaggedInventoryAdmin(admin.ModelAdmin):
    raw_id_fields = ('type', )

    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(TaggedInventory, TaggedInventoryAdmin)
