# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-24 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0124_auto_20160724_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='sats_article',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'currency'),
        ),
        migrations.AddField(
            model_name='sats_article_m',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
