# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-07 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectman', '0005_auto_20180607_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childtask',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
