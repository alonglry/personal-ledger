# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-10 01:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0142_auto_20160902_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='all_table_columns',
            name='definition',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name=b'definition'),
        ),
        migrations.AlterField(
            model_name='all_table_columns_m',
            name='definition',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
