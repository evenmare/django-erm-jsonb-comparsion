# Generated by Django 3.2.4 on 2022-12-27 20:44

import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('commons', '0002_initial_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaggedInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, verbose_name='Название')),
                ('tags', models.JSONField(verbose_name='Тэги')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_inventories', to='commons.type', verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Инвентарь с тэгами',
                'verbose_name_plural': 'Инвентарь с тэгами',
            },
        ),
        migrations.AddIndex(
            model_name='taggedinventory',
            index=django.contrib.postgres.indexes.GinIndex(django.db.models.expressions.F('tags'), name='tags_index'),
        ),
    ]