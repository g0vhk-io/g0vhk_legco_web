from django.db import models
from datetime import datetime
from bill_model import *
from common_models import *
# Create your models here.

class Motion(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    mover_type = models.CharField(max_length=512)
    mover_ch = models.CharField(max_length=512, default=None, null=True)
    mover_en = models.CharField(max_length=512, default=None, null=True)
    mover_individual = models.ForeignKey(Individual, null=True, blank=True)
    def __unicode__(self):
        return self.name_en + "-" + self.name_ch

class ImportantMotion(models.Model):
    motion = models.ForeignKey(Motion)

class Constituency(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    def __unicode__(self):
        return self.name_en + "-" + self.name_ch

class Meeting(models.Model):
    date = models.DateField()
    meeting_type = models.CharField(max_length=1024,default=None)
    key = models.CharField(max_length=255, default="no-key", blank=True, null=True, unique=True)
    source_url = models.CharField(max_length=2048, null=True)
    def __unicode__(self):
        return self.date.strftime('%Y-%m-%d') + "-" + str(self.source_url)

class Vote(models.Model):
    date = models.DateField()
    time = models.TimeField()
    vote_number = models.IntegerField()
    motion = models.ForeignKey(Motion)
    meeting = models.ForeignKey(Meeting)
    def __unicode__(self):
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
    def __unicode__(self):
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
    def __unicode__(self):
        return self.vote.motion.name_en + " " + self.individual.name_en + " " + self.result

class Question(models.Model):
    individual = models.ForeignKey(Individual)
    key = models.CharField(max_length=100, unique=True)
    date = models.DateField()
    question_type = models.CharField(max_length=255)
    link = models.CharField(max_length=1024, default="")
    question = models.TextField(max_length=33554432, default="")
    answer = models.TextField(max_length=33554432, default="")
    responder = models.CharField(max_length=255)
    question_type = models.CharField(max_length=512)
    title_ch = models.CharField(max_length=512, default="")
    keywords = models.ManyToManyField(Keyword)
    def __unicode__(self):
        return self.date.strftime("%Y-%m-%d") + self.individual.name_ch + self.title_ch

class MeetingSpeech(models.Model):
    individual = models.ForeignKey(Individual, null=True, blank=True)
    others_individual = models.ManyToManyField(Individual, related_name='others')
    title_ch = models.CharField(max_length=100)
    text_ch = models.TextField(max_length=33554432, default="")
    bookmark = models.CharField(max_length=100)
    sequence_number = models.IntegerField(default=0)


class MeetingPersonel(models.Model):
    individual = models.ForeignKey(Individual, null=True, blank=True)
    title_ch = models.CharField(max_length=100)

class MeetingHansard(models.Model):
    date = models.DateField()
    meeting_type = models.CharField(max_length=128, default="cm")
    key = models.CharField(max_length=128, unique=True)
    source_url = models.CharField(max_length=2048)
    speeches = models.ManyToManyField(MeetingSpeech)
    members_present = models.ManyToManyField(MeetingPersonel, related_name='present')
    members_absent = models.ManyToManyField(MeetingPersonel, related_name='absent')
    public_officers = models.ManyToManyField(MeetingPersonel, related_name='officers')
    clerks = models.ManyToManyField(MeetingPersonel, related_name='clerks')


class FinanceMeetingItem(models.Model):
    key = models.CharField(max_length=128, unique=True)
    description = models.CharField(max_length=2048)
    source = models.CharField(max_length=2048)
    keywords = models.ManyToManyField(Keyword)

class FinanceMeetingResult(models.Model):
    meeting = models.ForeignKey(Meeting, null=True, blank=True)
    key = models.CharField(max_length=128, unique=True)
    source = models.CharField(max_length=2048)

class FinanceMeetingItemEvent(models.Model):
    item = models.ForeignKey(FinanceMeetingItem)
    date = models.DateField()
    decision = models.CharField(max_length=128)
    vote = models.ForeignKey(Vote, null=True, blank=True)
    result = models.ForeignKey(FinanceMeetingResult, null=True, blank=True)


class Council(models.Model):
    name_en = models.CharField(max_length=512)
    name_ch = models.CharField(max_length=512)
    start_year = models.IntegerField(default=0)
    individuals = models.ManyToManyField(Individual)
    members = models.ManyToManyField(Individual, through='CouncilMember', related_name='member')
    chairman = models.ForeignKey(Individual, related_name='chair', null=True, blank=True)
    def __unicode__(self):
        return self.name_en + "-" + self.name_ch


class CouncilMembershipType(models.Model):
    GC = 'GC'
    FC_DC = 'FC_DC'
    FC = 'FC'
    CATEGORY_CHOICES = (
        (GC, 'Geographical Constituencies'),
        (FC_DC, 'Functional Constituency District Council (Second)'),
        (FC, 'Functional Constituency')
    )
    category = models.CharField(max_length=128, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=128)
    def __unicode__(self):
        return self.category + "-" + self.sub_category




class CouncilMember(models.Model):
    member = models.ForeignKey(Individual)
    council = models.ForeignKey(Council)
    membership_type = models.ForeignKey(CouncilMembershipType)
    def __unicode__(self):
        return self.member.name_ch + "-" + self.council.name_ch + "-" + unicode(self.membership_type) 



#
