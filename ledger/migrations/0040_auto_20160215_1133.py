# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-15 03:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ledger', '0039_auto_20160215_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='last_update_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]
