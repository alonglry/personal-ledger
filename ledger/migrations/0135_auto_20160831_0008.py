# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-30 16:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0134_auto_20160830_2252'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='all_table_columns',
            options={'ordering': ['project', 'model_file_name', 'table_name', 'column_name']},
        ),
    ]
