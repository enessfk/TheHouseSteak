# Generated by Django 3.0.4 on 2020-05-07 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_auto_20200507_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='slug',
            new_name='slugTitle',
        ),
    ]