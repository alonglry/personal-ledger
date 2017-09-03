# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-01 14:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0136_all_tables'),
    ]

    operations = [
        migrations.CreateModel(
            name='sats_barchart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t1', models.CharField(blank=True, max_length=5, null=True, verbose_name=b'today opinion')),
                ('y1', models.CharField(blank=True, max_length=5, null=True, verbose_name=b'yesterday opnion')),
                ('w1', models.CharField(blank=True, max_length=5, null=True, verbose_name=b'last week opinion')),
                ('m1', models.CharField(blank=True, max_length=5, null=True, verbose_name=b'last month opinion')),
                ('t2', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name=b'today opinion')),
                ('y2', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name=b'yesterday opnion')),
                ('w2', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name=b'last week opinion')),
                ('m2', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, verbose_name=b'last month opinion')),
                ('initial_price', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
                ('initial_date', models.DateField(blank=True, null=True)),
                ('max_price', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
                ('max_date', models.DateField(blank=True, null=True)),
                ('min_price', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
                ('min_date', models.DateField(blank=True, null=True)),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ledger.stock_company', to_field=b'ticker', verbose_name=b'ticker')),
            ],
            options={
                'verbose_name': 'barchart source',
            },
        ),
        migrations.CreateModel(
            name='sats_barchart_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker_id', models.CharField(blank=True, max_length=100, null=True)),
                ('t1', models.CharField(blank=True, max_length=5, null=True)),
                ('y1', models.CharField(blank=True, max_length=5, null=True)),
                ('w1', models.CharField(blank=True, max_length=5, null=True)),
                ('m1', models.CharField(blank=True, max_length=5, null=True)),
                ('t2', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('y2', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('w2', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('m2', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('initial_price', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
                ('initial_date', models.DateField(blank=True, null=True)),
                ('max_price', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
                ('max_date', models.DateField(blank=True, null=True)),
                ('min_price', models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True)),
                ('min_date', models.DateField(blank=True, null=True)),
                ('bk_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='sats_article_m',
            name='initial_price',
            field=models.DecimalField(blank=True, decimal_places=4, max_digits=9, null=True),
        ),
    ]
