# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 15:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0012_auto_20160102_2225'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'ordering': ['date', 'reference', 'balancesheet_type']},
        ),
    ]