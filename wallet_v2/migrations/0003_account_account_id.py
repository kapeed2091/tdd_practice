# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-22 15:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_v2', '0002_remove_account_account_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_id',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
