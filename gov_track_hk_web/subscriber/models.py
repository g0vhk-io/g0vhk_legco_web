from __future__ import unicode_literals

from django.db import models
from django import forms

# Create your models here.

class Subscriber(models.Model):
    email = models.EmailField(max_length=1024)
    key = models.CharField(unique=True, max_length=128)
    def __unicode__(self):
        return self.email


class News(models.Model):
    text_ch = models.TextField(max_length=4096)
    text_en = models.TextField(max_length=4096)
    title_ch = models.CharField(max_length=4096)
    title_en = models.CharField(max_length=4096)
    date = models.DateField()
    def __unicode__(self):
        return self.title_ch + " " + self.date.strftime('%Y-%m-%d')
