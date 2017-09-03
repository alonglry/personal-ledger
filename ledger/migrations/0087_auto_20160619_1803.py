# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-19 10:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0086_auto_20160619_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock_value',
            name='alpha_6',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'alpha 6'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='avg_daily_volume',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'avg daily volume'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='book_value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'book value'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='change',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'change'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='dividend_yield',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'dividend yield'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='dps',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'dividend per share'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='ebitda',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'ebitda'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='eps',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'earnings per share'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='market_cap',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'market cap'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='pe',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'price earnings ratio'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='peg',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'price earnings growth ratio'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='prev_close',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'previous close'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='price_book',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'price book'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='price_sales',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'price sales'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='short_ratio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'short ratio'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='stock_exchange',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'stock exchange'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='year_high',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'52w high'),
        ),
        migrations.AlterField(
            model_name='stock_value',
            name='year_low',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'52w low'),
        ),
    ]