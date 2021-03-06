# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-08-30 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0135_auto_20160831_0008'),
    ]

    operations = [
        migrations.CreateModel(
            name='all_tables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(blank=True, max_length=100, null=True)),
                ('model_file_name', models.CharField(blank=True, max_length=200, null=True)),
                ('table_name', models.CharField(blank=True, max_length=100, null=True)),
                ('verbose_name', models.CharField(blank=True, max_length=100, null=True)),
                ('verbose_name_plural', models.CharField(blank=True, max_length=100, null=True)),
                ('ordering', models.CharField(blank=True, max_length=200, null=True)),
                ('definition', models.CharField(blank=True, max_length=200, null=True)),
                ('if_migrated', models.CharField(blank=True, max_length=10, null=True)),
                ('last_update_date', models.DateTimeField(auto_now=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('model_form', models.CharField(blank=True, max_length=100, null=True)),
                ('backup', models.CharField(blank=True, max_length=10, null=True)),
                ('unicode', models.CharField(blank=True, max_length=200, null=True)),
                ('retention_d', models.IntegerField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'ordering': ['project', 'model_file_name', 'table_name'],
            },
        ),
    ]
