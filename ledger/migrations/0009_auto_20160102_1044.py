# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0008_auto_20160102_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='value_5',
            field=models.DateField(blank=True, null=True, verbose_name='date value'),
        ),
    ]
