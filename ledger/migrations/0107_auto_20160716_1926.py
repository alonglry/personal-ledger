# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-16 11:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0106_auto_20160716_1308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment_info',
            name='percentage',
        ),
        migrations.RemoveField(
            model_name='investment_info_m',
            name='percentage',
        ),
    ]