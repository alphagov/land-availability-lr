# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-04 14:02
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LRPoly',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('insert', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=1)),
                ('geom', django.contrib.gis.db.models.fields.GeometryField(geography=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Uprn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uprn', models.CharField(max_length=100, unique=True)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lr.LRPoly')),
            ],
        ),
    ]