# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-07-02 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0005_auto_20200621_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]
