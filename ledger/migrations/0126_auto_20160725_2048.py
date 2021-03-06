# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-25 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0125_auto_20160724_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sats_article',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='sats_article_m',
            name='currency',
        ),
        migrations.AlterField(
            model_name='stock_company',
            name='type',
            field=models.CharField(blank=True, choices=[(b'shares', b'shares'), (b'index', b'index'), (b'REIT', b'REIT'), (b'FX', b'FX'), (b'EFT', b'EFT'), (b'others', b'others')], max_length=100, null=True, verbose_name=b'type'),
        ),
        migrations.AlterField(
            model_name='stock_strategy',
            name='strategy',
            field=models.CharField(max_length=100),
        ),
    ]
