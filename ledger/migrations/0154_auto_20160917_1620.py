# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-17 08:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0153_auto_20160912_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='journal',
            name='test',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'test posting'),
        ),
        migrations.AddField(
            model_name='journal_m',
            name='test',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ledger',
            name='test',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'test posting'),
        ),
        migrations.AddField(
            model_name='ledger_m',
            name='test',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]