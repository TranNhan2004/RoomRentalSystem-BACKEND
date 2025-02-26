# Generated by Django 5.1.5 on 2025-02-26 16:34

import apps.rental_room.models
import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_room', '0003_rentalroom_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentalroomimage',
            name='image',
            field=models.ImageField(storage=storages.backends.s3.S3Storage(), upload_to=apps.rental_room.models.rental_room_image_upload_to),
        ),
    ]
