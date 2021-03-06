# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-24 13:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0123_auto_20160724_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sats_article_m',
            old_name='strategy',
            new_name='strategy_id',
        ),
        migrations.RenameField(
            model_name='sats_article_m',
            old_name='product',
            new_name='ticker_id',
        ),
        migrations.RemoveField(
            model_name='sats_article',
            name='product',
        ),
        migrations.RemoveField(
            model_name='sats_article',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='sats_article_m',
            name='product_type',
        ),
        migrations.RemoveField(
            model_name='sats_article_m',
            name='ticker',
        ),
        migrations.AlterField(
            model_name='sats_article',
            name='strategy',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ledger.stock_strategy', to_field=b'strategy', verbose_name=b'strategy'),
        ),
        migrations.AlterField(
            model_name='stock_strategy',
            name='strategy',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
