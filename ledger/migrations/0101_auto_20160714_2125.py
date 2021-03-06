# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-14 13:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0100_auto_20160713_2305'),
    ]

    operations = [
        migrations.CreateModel(
            name='investment_transaction_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('currency', models.CharField(blank=True, max_length=10, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('identifier_id', models.CharField(blank=True, max_length=50, null=True)),
                ('journal_id', models.CharField(blank=True, max_length=100, null=True)),
                ('remark', models.CharField(blank=True, max_length=500, null=True)),
                ('transaction_type_1', models.CharField(blank=True, max_length=50, null=True)),
                ('unit', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('bk_date', models.DateField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='investment_transaction',
            options={'ordering': ['date', 'identifier', 'transaction_type_1', 'transaction_type_2'], 'verbose_name': 'investment transaction', 'verbose_name_plural': 'investment transaction'},
        ),
        migrations.RemoveField(
            model_name='investment_transaction',
            name='price',
        ),
        migrations.RemoveField(
            model_name='investment_transaction',
            name='transaction_type_2',
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'amount'),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'currency'),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='date',
            field=models.DateField(verbose_name=b'date'),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='identifier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ledger.investment_info', to_field=b'identifier', verbose_name=b'ticker'),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='journal_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'journal ID'),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='remark',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name=b'remark'),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='transaction_type_1',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'transaction type 1'),
        ),
        migrations.AlterField(
            model_name='investment_transaction',
            name='unit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name=b'unit'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='value_5',
            field=models.DateField(blank=True, default=b'2016-07-14', null=True, verbose_name='date value'),
        ),
    ]
