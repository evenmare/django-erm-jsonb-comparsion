from django.db import models

from apps.commons.models import Type


class Tag(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Название',
    )
    data_type = models.CharField(
        max_length=7,
        default='str',
        null=False,
        blank=False,
        verbose_name='Тип данных',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
    
    def __str__(self) -> str:
        return f'{self.name}'


class Inventory(models.Model):
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
        related_name='inventories',
        verbose_name='Тип',
    )
    tags = models.ManyToManyField(
        Tag,
        through='InventoryTag',
        verbose_name='Тэги',
	)	
    
    class Meta:
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентари'
    
    def __str__(self) -> str:
        return f'{self.name}'


class InventoryTag(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tag_inventories',
        verbose_name='Тэгированный инвентарь',
    )
    inventory = models.ForeignKey(
        Inventory,
        on_delete=models.CASCADE,
        related_name='inventory_tags',
        verbose_name='Инвентарные тэги',
    )
    value = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Значение',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['inventory', 'tag'], name='inventory_tag_unique')
        ]

    def __str__(self) -> str:
        return f'{self.inventory} -> {self.tag}: {self.value}'
