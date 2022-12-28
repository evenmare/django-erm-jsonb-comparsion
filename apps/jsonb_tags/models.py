from django.db import models
from django.contrib.postgres.indexes import GinIndex

from apps.commons.models import Type


class TaggedInventory(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Название',
    )
    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='tagged_inventories',
        verbose_name='Тип',
    )
    tags = models.JSONField(verbose_name='Тэги')

    class Meta:
        indexes = [
            GinIndex('tags', name='tags_index'),
        ]
        verbose_name = 'Инвентарь с тэгами'
        verbose_name_plural = 'Инвентарь с тэгами'

    def __str__(self) -> str:
        return f'{self.name}'
