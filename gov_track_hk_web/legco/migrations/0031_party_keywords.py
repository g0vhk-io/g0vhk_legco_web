# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-13 16:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legco', '0030_auto_20160912_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='keywords',
            field=models.CharField(blank=True, default=None, max_length=512, null=True),
        ),
    ]
