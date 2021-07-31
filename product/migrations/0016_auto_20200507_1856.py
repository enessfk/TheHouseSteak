# Generated by Django 3.0.4 on 2020-05-07 15:56

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0015_auto_20200507_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, populate_from=('title', 'description')),
        ),
    ]
