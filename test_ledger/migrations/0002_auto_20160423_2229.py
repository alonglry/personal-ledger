# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-23 14:29
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('test_ledger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='map_acct_rollup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acct', models.IntegerField(unique=True, validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(99999)], verbose_name='GL account')),
                ('desc', models.CharField(max_length=200, verbose_name='description')),
                ('lvl1_cat', models.CharField(max_length=100, verbose_name='level 1 category')),
                ('lvl2_cat', models.CharField(max_length=100, verbose_name='level 2 category')),
                ('lvl3_cat', models.CharField(max_length=100, verbose_name='level 3 category')),
                ('lvl4_cat', models.CharField(max_length=100, verbose_name='level 4 category')),
                ('acct_owner', models.CharField(max_length=100, verbose_name='account owner')),
                ('lu_date', models.DateField(auto_now=True, verbose_name='last update date')),
                ('lu_user', models.CharField(max_length=50, verbose_name='last update user')),
            ],
            options={
                'ordering': ['acct'],
                'verbose_name': 'account rollup',
                'verbose_name_plural': 'accounts rollup',
            },
        ),
        migrations.AlterModelOptions(
            name='map_bu',
            options={'ordering': ['bu'], 'verbose_name': 'Business Unit', 'verbose_name_plural': 'Business Units'},
        ),
        migrations.AlterModelOptions(
            name='map_ledger',
            options={'ordering': ['ledger'], 'verbose_name': 'Ledger Book', 'verbose_name_plural': 'Ledger Books'},
        ),
        migrations.AddField(
            model_name='map_acct_rollup',
            name='bu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='test_ledger.map_bu', to_field='bu', verbose_name='business unit'),
        ),
        migrations.AddField(
            model_name='map_acct_rollup',
            name='ledger',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='test_ledger.map_ledger', to_field='ledger', verbose_name='ledger'),
        ),
    ]
