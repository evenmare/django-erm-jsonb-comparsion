from django.db import models


class Type(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        db_index=True,
        verbose_name='Название',
    )

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
    
    def __str__(self) -> str:
        return f'{self.name}'
