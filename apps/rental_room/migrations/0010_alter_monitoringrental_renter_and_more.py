# Generated by Django 5.1.5 on 2025-03-20 14:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_room', '0009_rename_is_sharable_roomcode_is_shared'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoringrental',
            name='renter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rented_rooms', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='monitoringrental',
            name='room_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monitoring_rentals', to='rental_room.roomcode'),
        ),
        migrations.AlterField(
            model_name='monthlyroominvoice',
            name='room_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='monthly_room_invoices', to='rental_room.roomcode'),
        ),
    ]
