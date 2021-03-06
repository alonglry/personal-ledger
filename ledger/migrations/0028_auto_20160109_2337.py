# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0027_auto_20160109_2246'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investment_info',
            old_name='last_updated_amount',
            new_name='last_update_amount',
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='identifier',
            field=models.CharField(default='', max_length=50, unique=True, verbose_name='ticker'),
            preserve_default=False,
        ),
    ]
