# Generated by Django 5.1.5 on 2025-02-10 15:10

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rental_room', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaveForLater',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('notes', models.CharField(blank=True, max_length=512, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rental_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_items', to='rental_room.rentalroom')),
            ],
        ),
    ]
