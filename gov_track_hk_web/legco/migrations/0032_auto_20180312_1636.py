# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-03-12 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legco', '0031_party_keywords'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsarticle',
            name='individuals',
        ),
        migrations.RemoveField(
            model_name='newsarticle',
            name='parties',
        ),
        migrations.AlterField(
            model_name='motion',
            name='mover_ch',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='motion',
            name='mover_en',
            field=models.CharField(default=None, max_length=512, null=True),
        ),
        migrations.DeleteModel(
            name='NewsArticle',
        ),
    ]
