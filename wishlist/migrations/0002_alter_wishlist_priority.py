# Generated by Django 5.1.2 on 2024-10-26 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='priority',
            field=models.CharField(blank=True, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='medium', max_length=6),
        ),
    ]
