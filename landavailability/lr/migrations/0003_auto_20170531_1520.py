# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-31 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lr', '0002_auto_20170515_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uprn',
            name='title',
        ),
        migrations.AddField(
            model_name='uprn',
            name='titles',
            field=models.ManyToManyField(related_name='uprns', to='lr.Title'),
        ),
    ]
