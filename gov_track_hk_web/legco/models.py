from django.db import models
from datetime import datetime
# Create your models here.

class Party(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    image = models.CharField(max_length=512)
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
    mover_ch = models.CharField(max_length=512, default=None)
    mover_en = models.CharField(max_length=512, default=None)
    mover_individual = models.ForeignKey(Individual, null=True, blank=True)
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
    meeting_type = models.CharField(max_length=1024,default=None)
    source_url = models.CharField(max_length=2048, null=True, unique=True)
    def __str__(self):
        return self.date.strftime('%Y-%m-%d') + "-" + str(self.source_url)

class Vote(models.Model):
    date = models.DateField()
    time = models.TimeField()
    vote_number = models.IntegerField()
    motion = models.ForeignKey(Motion)
    meeting = models.ForeignKey(Meeting)
    def __str__(self):
        return self.motion.name_en + " " + self.meeting.date.strftime("%Y-%m-%d")

class VoteSummary(models.Model):
    FUNCTIONAL = 'FUNC'
    OVERALL = 'OVER'
    GEOGRAPHICAL = 'GEOG'
    SUMMARY_CHOICES = ((FUNCTIONAL, 'Functional'),(OVERALL,'Overall'), (GEOGRAPHICAL, 'GEOG'))
    vote = models.ForeignKey(Vote,default=None)
    summary_type = models.CharField(max_length=64, choices = SUMMARY_CHOICES)
    present_count = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    yes_count = models.IntegerField(default=0)
    no_count = models.IntegerField(default=0)
    abstain_count = models.IntegerField(default=0)
    result = models.CharField(max_length=512)
    def __str__(self):
        return self.vote.motion.name_en +  " " + self.summary_type + " " + self.result

class IndividualVote(models.Model):
    individual = models.ForeignKey(Individual)
    YES = 'YES'
    NO = 'NO'
    ABSENT = 'ABSENT'
    ABSTAIN = 'ABSTAIN'
    VOTE_CHOICES = ((YES, 'Yes'), (NO, 'No'),(ABSENT, 'Absent'), (ABSTAIN, 'Abstain'))
    result = models.CharField(max_length=64, choices = VOTE_CHOICES, default=NO)
    vote = models.ForeignKey(Vote)
    def __str__(self):
        return self.vote.motion.name_en + " " + self.individual.name_en + " " + self.result

class NewsArticle(models.Model):
    individuals = models.ManyToManyField(Individual)
    parties = models.ManyToManyField(Party)
    link = models.CharField(max_length=2048, unique=True)
    title = models.CharField(max_length=2048)
    text = models.TextField(max_length=33554432, default="")
    image = models.TextField(max_length=33554432, default=None, blank=True, null=True)
    source = models.CharField(max_length=256)
    def __str__(self):
        return self.source + " " + self.title
