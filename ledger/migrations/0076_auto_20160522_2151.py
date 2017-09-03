# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-22 13:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0075_auto_20160522_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='sats_article',
            name='ticker',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'ticker'),
        ),
        migrations.AddField(
            model_name='sats_article',
            name='trend',
            field=models.URLField(blank=True, null=True, verbose_name=b'price trend'),
        ),
    ]
