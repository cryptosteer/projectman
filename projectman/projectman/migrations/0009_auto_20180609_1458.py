# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-09 14:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectman', '0008_merge_20180609_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='methodology',
            field=models.CharField(default='sin', max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='resources',
            field=models.TextField(default='n'),
        ),
        migrations.AlterField(
            model_name='task',
            name='state',
            field=models.IntegerField(choices=[(1, 'Done'), (2, 'In-progess'), (3, 'To-do')]),
        ),
    ]