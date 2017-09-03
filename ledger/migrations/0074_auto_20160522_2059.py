# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-22 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0073_auto_20160522_0152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sats_article',
            options={'verbose_name': 'stock article tracking article'},
        ),
        migrations.AlterModelOptions(
            name='sats_source',
            options={'verbose_name': 'stock article tracking source'},
        ),
        migrations.RemoveField(
            model_name='sats_source',
            name='fail_count',
        ),
        migrations.RemoveField(
            model_name='sats_source',
            name='pass_count',
        ),
        migrations.RemoveField(
            model_name='sats_source',
            name='total_count',
        ),
        migrations.RemoveField(
            model_name='sats_source',
            name='validation_count',
        ),
        migrations.AddField(
            model_name='sats_article',
            name='product',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'product'),
        ),
        migrations.AddField(
            model_name='sats_article',
            name='product_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'product type'),
        ),
        migrations.AlterField(
            model_name='sats_article',
            name='screenshot',
            field=models.ImageField(blank=True, default=b'ledger/image/no-image.jpg', null=True, upload_to=b'ledger/image/sats', verbose_name=b'screenshot'),
        ),
    ]
