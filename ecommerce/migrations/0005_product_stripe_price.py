# Generated by Django 5.0.4 on 2024-06-18 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_alter_pricehistory_date_alter_pricehistory_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
