# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-24 06:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0010_transaction_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='type',
            new_name='transaction_type',
        ),
    ]
