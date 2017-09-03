# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_ledger', '0007_auto_20160504_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map_acct_rollup',
            name='lu_date',
            field=models.DateField(auto_now=True, choices=[b'auto now', b'auto now'], null=True, verbose_name=b'last update date'),
        ),
        migrations.AlterField(
            model_name='map_acct_rollup',
            name='statement',
            field=models.CharField(blank=True, choices=[(b'balancesheet', b'balancesheet'), (b'income statement', b'income statement')], max_length=100, null=True, verbose_name=b'financial statement'),
        ),
    ]