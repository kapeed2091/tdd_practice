# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-22 15:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_v2', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_id',
        ),
    ]