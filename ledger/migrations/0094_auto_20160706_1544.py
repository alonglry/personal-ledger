# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-06 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0093_auto_20160706_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='cashflow_old',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_medisave', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('cpf_ordinary', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('cpf_special', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('dividendcard', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('investment', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('month', models.IntegerField(blank=True, null=True)),
                ('phone', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('rental', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('salary', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('saving', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('bk_date', models.DateField()),
            ],
        ),
        migrations.DeleteModel(
            name='cashflow_m',
        ),
    ]