# Generated by Django 3.0.4 on 2020-03-28 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20200327_2010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('keywords', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=250)),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('price', models.FloatField()),
                ('amount', models.IntegerField()),
                ('detail', models.TextField()),
                ('statu', models.CharField(choices=[('True', 'Yes'), ('False', 'No')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.Category')),
            ],
        ),
    ]