# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-24 09:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_v2', '0011_auto_20190123_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='transaction_date',
            new_name='transaction_date_time',
        ),
    ]
