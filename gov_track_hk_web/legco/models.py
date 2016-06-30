from django.db import models
from datetime import datetime
# Create your models here.

class Party(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    def __str__(self):
        return self.name_en + "-" + self.name_ch

class Individual(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    party = models.ForeignKey(Party, null=True, blank=True)
    def __str__(self):
        return self.name_en + "-" + self.name_ch

class Motion(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    mover_type = models.CharField(max_length=512)
    mover_individual = models.ForeignKey(Individual)
    def __str__(self):
        return self.name_en + "-" + self.name_ch

class Constituency(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    def __str__(self):
        return self.name_en + "-" + self.name_ch

class Council(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    start_year = models.IntegerField(default=0)
    def __str__(self):
        return self.name_en + "-" + self.name_ch

class Meeting(models.Model):
    date = models.DateField()
    time = models.TimeField()
    separate = models.BooleanField()
    motion = models.ForeignKey(Motion)
    def __str__(self):
        return self.date.strftime('%Y-%m-%d') + "-" + str(self.motion)

class VoteSummary(models.Model):
    FUNCTIONAL = 'FUNC'
    OVERALL = 'OVER'
    GEOGRAPHICAL = 'GEOG'
    SUMMARY_CHOICES = ((FUNCTIONAL, 'Functional'),(OVERALL,'Overall'), (GEOGRAPHICAL, 'GEOG'))
    meeting = models.ForeignKey(Meeting,default=None)
    summary_type = models.CharField(max_length=64, choices = SUMMARY_CHOICES)
    present_count = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    yes_count = models.IntegerField(default=0)
    no_count = models.IntegerField(default=0)
    abstain_count = models.IntegerField(default=0)
    result = models.CharField(max_length=512)

class IndividualVote(models.Model):
    individual = models.ForeignKey(Individual)
    YES = 'YES'
    NO = 'NO'
    ABSENT = 'ABSENT'
    VOTE_CHOICES = ((YES, 'Yes'), (NO, 'No'),(ABSENT, 'Absent'))
    vote = models.CharField(max_length=64, choices = VOTE_CHOICES)

