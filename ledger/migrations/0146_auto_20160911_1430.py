# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-11 06:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0145_auto_20160911_1420'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='all_table_columns',
            options={'ordering': ['project', 'model_file_name', 'table_name', 'sn', 'column_name'], 'verbose_name': 'all table column', 'verbose_name_plural': 'all table columns'},
        ),
    ]
