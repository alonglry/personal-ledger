# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0019_remove_investment_transaction_exchange_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment_transaction',
            name='product_description',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
