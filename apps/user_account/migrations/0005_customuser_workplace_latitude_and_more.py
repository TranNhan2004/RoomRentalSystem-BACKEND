# Generated by Django 5.1.5 on 2025-03-05 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account_app_label', '0004_remove_customuser_account_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='workplace_latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='workplace_longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
