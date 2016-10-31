from django.db import models
from datetime import datetime

class Consultation(models.Model):
    lang = models.CharField(max_length=128)
    date = models.DateTimeField()
    link = models.CharField(max_length=1024)
    key = models.CharField(max_length=128)
    title = models.CharField(max_length=1024)
    class Meta:
        unique_together = ('lang', 'key')
    def __unicode__(self):
        return self.link + "-" + self.title.encode("utf-8") + "-" + self.lang


