# Generated by Django 4.0.4 on 2022-04-27 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busAgency', '0005_alter_driver_dni_alter_passenger_dni'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='is_working',
            field=models.BooleanField(default=False),
        ),
    ]
