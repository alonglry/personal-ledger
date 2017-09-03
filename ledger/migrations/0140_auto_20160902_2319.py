# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-09-02 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0139_auto_20160902_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='all_table_columns_m',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project', models.CharField(blank=True, max_length=100, null=True)),
                ('model_file_name', models.CharField(blank=True, max_length=100, null=True)),
                ('table_name', models.CharField(blank=True, max_length=100, null=True)),
                ('column_name', models.CharField(blank=True, max_length=10, null=True)),
                ('verbose_name', models.CharField(blank=True, max_length=10, null=True)),
                ('verbose_name_plural', models.CharField(blank=True, max_length=100, null=True)),
                ('data_type', models.CharField(blank=True, max_length=100, null=True)),
                ('min_length', models.CharField(blank=True, max_length=10, null=True)),
                ('max_length', models.CharField(blank=True, max_length=10, null=True)),
                ('definition', models.CharField(blank=True, max_length=20, null=True)),
                ('choice_options', models.CharField(blank=True, max_length=500, null=True)),
                ('foreign_key_table', models.CharField(blank=True, max_length=200, null=True)),
                ('foreign_key_column', models.CharField(blank=True, max_length=200, null=True)),
                ('foreign_key_on_delete', models.CharField(blank=True, max_length=10, null=True)),
                ('nullable', models.CharField(blank=True, max_length=10, null=True)),
                ('blank', models.CharField(blank=True, max_length=10, null=True)),
                ('unique_key', models.CharField(blank=True, max_length=10, null=True)),
                ('remark', models.CharField(blank=True, max_length=500, null=True)),
                ('if_migrated', models.CharField(blank=True, max_length=10, null=True)),
                ('last_update_date', models.DateTimeField(blank=True, null=True)),
                ('default_value', models.CharField(blank=True, max_length=100, null=True)),
                ('auto_save_foreign_key', models.CharField(blank=True, max_length=1, null=True)),
                ('decimal_place', models.CharField(blank=True, max_length=100, null=True)),
                ('model_form', models.CharField(blank=True, max_length=100, null=True)),
                ('path', models.CharField(blank=True, max_length=50, null=True)),
                ('bk_date', models.DateField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='all_table_columns',
            options={'ordering': ['project', 'model_file_name', 'table_name', 'column_name'], 'verbose_name': 'all table columns'},
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='auto_save_foreign_key',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name=b'auto save foreign key'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='blank',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'blank'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='choice_options',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name=b'choice options'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='column_name',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'column name'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='data_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'data type'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='decimal_place',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'decimal place'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='default_value',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'default value'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='definition',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name=b'definition'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='foreign_key_column',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name=b'foreign key column'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='foreign_key_on_delete',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'foreign key on delete'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='foreign_key_table',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name=b'foreign key table'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='if_migrated',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'if migrated'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='last_update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=b'last update date'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='max_length',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'max length'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='min_length',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'min length'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='model_file_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'model file name'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='model_form',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'model form'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='nullable',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'nullable'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='path',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name=b'path'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='project',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'project'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='remark',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name=b'remark'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='table_name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'table name'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='unique_key',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'unique key'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='verbose_name',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'verbose name'),
        ),
        migrations.AlterField(
            model_name='all_table_columns',
            name='verbose_name_plural',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name=b'verbose name plural'),
        ),
        migrations.AlterField(
            model_name='all_tables',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name=b'last update date'),
        ),
    ]