# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-06-12 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20190816_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_delivery',
            field=models.BooleanField(default=False),
        ),
    ]
