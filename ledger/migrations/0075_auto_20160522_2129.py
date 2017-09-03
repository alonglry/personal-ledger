# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-22 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0074_auto_20160522_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='sats_source',
            name='fail_count',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'failed number'),
        ),
        migrations.AddField(
            model_name='sats_source',
            name='pass_count',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'passed number'),
        ),
        migrations.AddField(
            model_name='sats_source',
            name='total_count',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'total number'),
        ),
        migrations.AddField(
            model_name='sats_source',
            name='validation_count',
            field=models.IntegerField(blank=True, null=True, verbose_name=b'validated number'),
        ),
    ]