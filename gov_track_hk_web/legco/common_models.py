from django.db import models
from datetime import datetime

class Keyword(models.Model):
    keyword = models.CharField(max_length=128, unique=True)
    def __unicode__(self):
        return self.keyword

class Party(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    image = models.CharField(max_length=512, blank=True, null=True, default=None)
    def __unicode__(self):
        return self.name_en + "-" + self.name_ch

class Individual(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    party = models.ForeignKey(Party, null=True, blank=True)
    image = models.CharField(max_length=512, blank=True, null=True, default=None)
    def __unicode__(self):
        return self.name_en + "-" + self.name_ch


