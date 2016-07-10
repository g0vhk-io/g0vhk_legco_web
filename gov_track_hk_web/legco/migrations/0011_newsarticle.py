# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-07 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('legco', '0010_party_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=2048)),
                ('title', models.CharField(max_length=2048)),
                ('source', models.CharField(max_length=256)),
                ('individuals', models.ManyToManyField(to='legco.Individual')),
            ],
        ),
    ]
