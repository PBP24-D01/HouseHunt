# Generated by Django 5.1.2 on 2024-10-27 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iklan', '0007_alter_iklanentry_banner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iklanentry',
            name='banner',
            field=models.ImageField(default=1, upload_to='banner/'),
            preserve_default=False,
        ),
    ]
