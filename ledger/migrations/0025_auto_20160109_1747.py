# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-09 09:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0024_auto_20160109_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment_transaction',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='identifier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ledger.investment_info', to_field='identifier'),
        ),
    ]
