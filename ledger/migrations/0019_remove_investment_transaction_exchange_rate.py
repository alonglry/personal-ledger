# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 07:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0018_auto_20160109_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment_transaction',
            name='exchange_rate',
        ),
    ]
