# Generated by Django 5.1.2 on 2024-10-27 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iklan', '0005_rename_user_iklanentry_seller_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iklanentry',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
    ]
