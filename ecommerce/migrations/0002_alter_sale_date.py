# Generated by Django 5.0.4 on 2024-05-10 00:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 9, 21, 14, 12, 279445)),
        ),
    ]