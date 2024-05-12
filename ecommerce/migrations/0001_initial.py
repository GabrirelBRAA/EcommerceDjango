# Generated by Django 5.0.4 on 2024-05-10 00:11

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('marca', models.CharField(max_length=200, null=True)),
                ('rating', models.FloatField(default=0, validators=[django.core.validators.MaxValueValidator(5.0), django.core.validators.MinValueValidator(0.0)])),
                ('description', models.TextField(default='')),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.FloatField()),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ecommerce.category')),
            ],
        ),
        migrations.CreateModel(
            name='PriceHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.product')),
            ],
            options={
                'verbose_name_plural': 'price histories',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/')),
                ('priority', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product')),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2024, 5, 9, 21, 11, 39, 450185))),
                ('status', models.CharField(choices=[('COMP', 'Complete'), ('PPND', 'Payment Pending'), ('DPND', 'Delivery Pending'), ('CANC', 'Cancelled'), ('CPND', 'Cancelled With Pending Refund')], default='PPND', max_length=4)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ecommerce.sale')),
            ],
        ),
    ]
