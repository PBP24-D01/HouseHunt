# Generated by Django 5.1.2 on 2024-10-26 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HouseHuntAuth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='stars',
            field=models.IntegerField(default=0),
        ),
    ]