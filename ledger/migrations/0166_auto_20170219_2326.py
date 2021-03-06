# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-02-19 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0165_ema_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='ema_value',
            name='ticker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ledger.stock_company', to_field=b'ticker', verbose_name=b'ticker'),
        ),
        migrations.AlterField(
            model_name='ema_value',
            name='tickerdate',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ledger.stock_value', to_field=b'tickerdate', unique=True, verbose_name=b'ticker date identifier'),
        ),
    ]
