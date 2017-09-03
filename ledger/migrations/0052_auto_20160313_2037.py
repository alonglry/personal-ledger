# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-13 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0051_auto_20160313_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment_info',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=4, default=0.0, max_digits=10, null=True),
        ),
    ]
