# Generated by Django 4.2.11 on 2024-03-18 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speech',
            name='from_time',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Время начала'),
        ),
        migrations.AlterField(
            model_name='speech',
            name='to_time',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Время конца'),
        ),
    ]