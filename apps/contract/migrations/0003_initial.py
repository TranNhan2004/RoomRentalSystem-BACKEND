# Generated by Django 5.1.5 on 2025-02-05 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contract', '0002_initial'),
        ('user_account_app_label', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalcontract',
            name='rented_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rented_contracts', to='user_account_app_label.renter'),
        ),
        migrations.AddConstraint(
            model_name='rentalcontract',
            constraint=models.CheckConstraint(condition=models.Q(('end_date__gt', models.F('start_date'))), name='__RENTAL_CONTRACT__end_date__gt__start_date'),
        ),
    ]
