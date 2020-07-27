# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-06-12 13:16
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):
    dependencies = [
        ('products', '0011_product_is_digital'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(storage=django.core.files.storage.FileSystemStorage(
                    location='/mnt/c/Users/permi/source/repos/draft/2/static_cdn/protected_media'),
                                          upload_to=products.models.upload_product_file_loc)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
    ]
