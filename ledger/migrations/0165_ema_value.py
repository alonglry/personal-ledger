# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-02-19 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0164_auto_20170219_1352'),
    ]

    operations = [
        migrations.CreateModel(
            name='ema_value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ema5', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'5 day EMA')),
                ('ema10', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'10 day EMA')),
                ('tickerdate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ledger.stock_value', to_field=b'tickerdate', verbose_name=b'ticker date identifier')),
            ],
            options={
                'verbose_name': 'stock EMA value',
            },
        ),
    ]
