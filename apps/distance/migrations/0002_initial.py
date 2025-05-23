# Generated by Django 5.1.5 on 2025-03-13 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('distance', '0001_initial'),
        ('rental_room', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='distance',
            name='rental_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distances', to='rental_room.rentalroom'),
        ),
        migrations.AddField(
            model_name='distance',
            name='renter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='distances', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='distance',
            constraint=models.UniqueConstraint(fields=('rental_room', 'renter'), name='__DISTANCE__rental_room_renter__unique_together'),
        ),
    ]
