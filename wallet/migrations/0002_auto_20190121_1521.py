# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-01-21 09:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='customer_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]