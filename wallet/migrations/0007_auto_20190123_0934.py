# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-23 04:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0006_auto_20190122_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_id',
            field=models.CharField(max_length=20),
        ),
    ]
