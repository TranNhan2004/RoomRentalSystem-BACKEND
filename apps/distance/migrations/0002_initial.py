# Generated by Django 5.1.5 on 2025-02-05 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('distance', '0001_initial'),
        ('rental_room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='distance',
            name='rental_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distances', to='rental_room.rentalroom'),
        ),
    ]
