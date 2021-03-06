# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-20 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0054_auto_20160320_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account_info',
            name='amount',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=10),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='currency',
            field=models.CharField(default='SGD', max_length=10),
        ),
        migrations.AlterField(
            model_name='account_info',
            name='number',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='account_info',
            name='type',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
