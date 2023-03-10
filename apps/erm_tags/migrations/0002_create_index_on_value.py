# Generated by Django 3.2.4 on 2022-12-28 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commons', '0002_initial_data'),
        ('erm_tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventories', to='commons.type', verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='inventorytag',
            name='value',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Значение'),
        ),
    ]
