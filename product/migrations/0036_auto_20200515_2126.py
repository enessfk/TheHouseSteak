# Generated by Django 3.0.4 on 2020-05-15 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0035_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=250),
        ),
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='comment',
            name='subject',
            field=models.CharField(max_length=50),
        ),
    ]