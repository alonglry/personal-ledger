# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-21 16:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0071_auto_20160521_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='value_5',
            field=models.DateField(blank=True, default=b'2016-05-22', null=True, verbose_name='date value'),
        ),
        migrations.AlterField(
            model_name='sats_article',
            name='screenshot',
            field=models.ImageField(blank=True, default=b'ledger/no-image.jpg', null=True, upload_to=b'ledger/image/sats', verbose_name=b'screenshot'),
        ),
    ]