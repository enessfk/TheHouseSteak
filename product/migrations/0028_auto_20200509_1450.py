# Generated by Django 3.0.4 on 2020-05-09 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_auto_20200509_1443'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='level',
        ),
        migrations.RemoveField(
            model_name='category',
            name='lft',
        ),
        migrations.RemoveField(
            model_name='category',
            name='rght',
        ),
        migrations.RemoveField(
            model_name='category',
            name='tree_id',
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.Category'),
        ),
    ]
