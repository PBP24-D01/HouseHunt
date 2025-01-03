# Generated by Django 5.1.2 on 2024-10-25 16:37
# Generated by Django 5.1.2 on 2024-10-25 05:37

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='House',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul', models.CharField(max_length=100)),
                ('deskripsi', models.CharField(max_length=255)),
                ('harga', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('lokasi', models.CharField(max_length=100)),
                ('gambar', models.ImageField(upload_to='static/img/')),
                ('kamar_tidur', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('kamar_mandi', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('is_available', models.BooleanField(default=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
