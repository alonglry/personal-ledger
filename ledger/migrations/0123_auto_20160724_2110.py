# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-24 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0121_auto_20160724_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='sats_article',
            name='lower_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'lower price'),
        ),
        migrations.AddField(
            model_name='sats_article',
            name='upper_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'upper price'),
        ),
        migrations.AddField(
            model_name='sats_article_m',
            name='lower_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AddField(
            model_name='sats_article_m',
            name='upper_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
