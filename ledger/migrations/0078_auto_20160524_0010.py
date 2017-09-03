# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-23 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0077_auto_20160523_2252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='value_5',
            field=models.DateField(blank=True, default=b'2016-05-24', null=True, verbose_name='date value'),
        ),
        migrations.AlterField(
            model_name='sats_article',
            name='product_type',
            field=models.CharField(blank=True, choices=[(b'shares', b'shares'), (b'funds', b'funds'), (b'index', b'index'), (b'FX', b'FX'), (b'others', b'others')], max_length=100, null=True, verbose_name=b'product type'),
        ),
    ]
