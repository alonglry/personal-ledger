# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-12 04:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0152_auto_20160912_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment_info',
            name='broker_company',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'broker company'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='paid_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name=b'purchasing cost'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='profit_loss',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name=b'profit/losss'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='total_profit_loss',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True, verbose_name=b'net profit'),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='broker_company',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'broker company'),
        ),
    ]
