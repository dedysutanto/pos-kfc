# Generated by Django 4.0.6 on 2022-07-20 05:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sales.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('items', '0001_initial'),
        ('shops', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('cashier', models.ForeignKey(limit_choices_to=sales.models.Receipts.limit_choices_to_current_user, on_delete=django.db.models.deletion.RESTRICT, to='shops.cashiers', verbose_name='Cashier')),
                ('shop', models.ForeignKey(limit_choices_to=sales.models.Receipts.limit_choices_to_current_user, on_delete=django.db.models.deletion.RESTRICT, to='shops.shops', verbose_name='Shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'receipt',
                'verbose_name_plural': 'receipts',
                'db_table': 'receipts',
            },
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=1, verbose_name='Amount')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(limit_choices_to=sales.models.Sales.limit_choices_to_current_user, on_delete=django.db.models.deletion.RESTRICT, to='items.categories', verbose_name='Category')),
                ('item', models.ForeignKey(limit_choices_to=sales.models.Sales.limit_choices_to_current_user, on_delete=django.db.models.deletion.RESTRICT, to='items.items', verbose_name='Item')),
                ('receipt', models.ForeignKey(limit_choices_to=sales.models.Sales.limit_choices_to_current_user, on_delete=django.db.models.deletion.RESTRICT, to='sales.receipts', verbose_name='Receipt')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'sale',
                'verbose_name_plural': 'sales',
                'db_table': 'sales',
            },
        ),
    ]
