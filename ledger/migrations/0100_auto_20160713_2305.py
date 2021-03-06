# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-13 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0099_auto_20160713_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='investment_info_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commission', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('company', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('currency', models.CharField(blank=True, max_length=10, null=True)),
                ('current_amount', models.CharField(blank=True, max_length=100, null=True)),
                ('current_price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('dividend', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('identifier', models.CharField(blank=True, max_length=50, null=True)),
                ('last_update_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('paid_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('profit_loss', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('remark', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('sold_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total_profit_loss', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('total_yield', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('type', models.CharField(blank=True, max_length=50, null=True)),
                ('unit', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('bk_date', models.DateField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='investment_info',
            options={'ordering': ['company', 'identifier'], 'verbose_name': 'investment account detail', 'verbose_name_plural': 'investment account details'},
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='commission',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'commission'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='company',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'company'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'country'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='currency',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'currency'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='current_amount',
            field=models.CharField(blank=True, default=b'0', max_length=100, null=True, verbose_name=b'current value'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='current_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=b'0', max_digits=8, null=True, verbose_name=b'current price'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='dividend',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'dividend'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='last_update_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'last update amount'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='paid_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'purchasing expense'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'percentage'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='profit_loss',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'profit/loss'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='remark',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'remark'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='sold_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'selling income'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='total_profit_loss',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'net profit/loss'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='total_yield',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'yield'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='type',
            field=models.CharField(blank=True, choices=[(b'shares', b'shares'), (b'funds', b'funds')], max_length=50, null=True, verbose_name=b'type'),
        ),
        migrations.AlterField(
            model_name='investment_info',
            name='unit',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name=b'unit'),
        ),
    ]
