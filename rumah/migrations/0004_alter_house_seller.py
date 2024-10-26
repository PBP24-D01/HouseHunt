# Generated by Django 5.1.2 on 2024-10-26 08:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseHuntAuth', '0001_initial'),
        ('rumah', '0003_alter_house_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HouseHuntAuth.seller'),
        ),
    ]