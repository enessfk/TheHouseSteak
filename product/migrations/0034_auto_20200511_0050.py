# Generated by Django 3.0.4 on 2020-05-10 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0033_auto_20200510_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ingredients',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
