# Generated by Django 4.0.6 on 2022-07-19 07:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import employees.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shops', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Employee Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('telephone', models.CharField(blank=True, max_length=50, verbose_name='Telephone')),
                ('pin', models.CharField(max_length=6, verbose_name='Cashier PIN')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('shops', models.ManyToManyField(limit_choices_to=employees.models.Employees.limit_choices_to_current_user, to='shops.shops')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
                'db_table': 'employees',
            },
        ),
    ]
