# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-02 02:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0009_auto_20160102_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='value_5',
            field=models.DateField(blank=True, default=b'2016-01-02', null=True, verbose_name='date value'),
        ),
    ]
