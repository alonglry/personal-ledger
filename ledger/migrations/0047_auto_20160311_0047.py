# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-10 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0046_auto_20160310_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashflow',
            name='saving',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='value_5',
            field=models.DateField(blank=True, default=b'2016-03-11', null=True, verbose_name='date value'),
        ),
    ]
