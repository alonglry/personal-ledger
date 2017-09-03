# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-18 08:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0080_auto_20160526_2349'),
    ]

    operations = [
        migrations.CreateModel(
            name='stock_company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name=b'company')),
                ('country', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'country')),
                ('exchange', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'exchange')),
                ('ticker', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name=b'ticker')),
            ],
            options={
                'verbose_name': 'stock company',
                'verbose_name_plural': 'stock companies',
            },
        ),
        migrations.CreateModel(
            name='stock_company_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('exchange', models.CharField(blank=True, max_length=100, null=True)),
                ('ticker', models.CharField(blank=True, max_length=100, null=True)),
                ('bk_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='stock_dimension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alphas_num', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'101_formulaic_alphas_num')),
                ('alphas_type', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'101_formulaic_alphas_type')),
                ('data_type', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'data_type')),
                ('descr', models.CharField(blank=True, max_length=500, null=True, verbose_name=b'description')),
                ('dim', models.CharField(max_length=100, unique=True, verbose_name=b'dimension')),
                ('remark', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'remark')),
                ('src', models.CharField(blank=True, max_length=100, null=True, verbose_name=b'source')),
            ],
            options={
                'verbose_name': 'stock dimension',
            },
        ),
        migrations.CreateModel(
            name='stock_dimension_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alphas_num', models.CharField(blank=True, max_length=100, null=True)),
                ('alphas_type', models.CharField(blank=True, max_length=100, null=True)),
                ('data_type', models.CharField(blank=True, max_length=100, null=True)),
                ('descr', models.CharField(blank=True, max_length=500, null=True)),
                ('dim', models.CharField(blank=True, max_length=100, null=True)),
                ('remark', models.CharField(blank=True, max_length=100, null=True)),
                ('src', models.CharField(blank=True, max_length=100, null=True)),
                ('bk_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='stock_value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adj_close', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'adjusted close price')),
                ('alpha_6', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'alpha 6')),
                ('close', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'close price')),
                ('date', models.DateField(blank=True, null=True, verbose_name=b'date')),
                ('high', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'high')),
                ('low', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'low')),
                ('open', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'open price')),
                ('volume', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(99999999)], verbose_name=b'valume')),
                ('ticker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ledger.stock_company', to_field=b'ticker', verbose_name=b'ticker')),
            ],
            options={
                'verbose_name': 'stock value',
            },
        ),
        migrations.CreateModel(
            name='stock_value_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adj_close', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('alpha_6', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('close', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('high', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('low', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('open', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('ticker_id', models.CharField(blank=True, max_length=10, null=True)),
                ('volume', models.IntegerField(blank=True, null=True)),
                ('bk_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='account_info',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=b'0', max_digits=8, null=True, verbose_name=b'account balance'),
        ),
        migrations.AlterField(
            model_name='account_info_m',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='journal',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
        migrations.AlterField(
            model_name='journal_m',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='value_5',
            field=models.DateField(blank=True, default=b'2016-06-18', null=True, verbose_name='date value'),
        ),
    ]