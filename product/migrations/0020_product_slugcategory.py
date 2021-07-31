# Generated by Django 3.0.4 on 2020-05-07 16:16

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0019_auto_20200507_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slugCategory',
            field=autoslug.fields.AutoSlugField(blank=True, editable=False, populate_from='category', unique_with=('created_at',)),
        ),
    ]