# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-02 12:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_ledger', '0003_auto_20160502_2018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='map_acct_rollup',
            old_name='desc',
            new_name='descr',
        ),
    ]
