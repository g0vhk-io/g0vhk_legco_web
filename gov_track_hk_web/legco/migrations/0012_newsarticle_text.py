# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 15:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legco', '0011_newsarticle'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsarticle',
            name='text',
            field=models.TextField(default='', max_length=33554432),
        ),
    ]
