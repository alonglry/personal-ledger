# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-26 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0078_auto_20160524_0010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journal',
            options={'verbose_name': 'journal'},
        ),
        migrations.AlterField(
            model_name='parameter',
            name='value_5',
            field=models.DateField(blank=True, default=b'2016-05-26', null=True, verbose_name='date value'),
        ),
    ]
