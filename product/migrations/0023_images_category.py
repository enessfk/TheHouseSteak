# Generated by Django 3.0.4 on 2020-05-09 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_product_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.Category'),
        ),
    ]
