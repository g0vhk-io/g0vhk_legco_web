# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Count
from legco.models import Individual, Party, IndividualVote, Vote, VoteSummary, Bill,  MeetingSpeech, MeetingHansard, FinanceMeetingItem, FinanceMeetingItemEvent, FinanceMeetingResult, Question, BillCommittee, Council, CouncilMember, CouncilMembershipType
from legco.models import ImportantMotion
from datetime import date, datetime
from django.db.models import Q
from legco.models import MeetingSpeech, MeetingPersonel, MeetingHansard
from collections import defaultdict
from django.http import HttpResponse
from legco.templatetags import legco_extras
from urllib.parse import urljoin
from math import cos, sin, pi
import textwrap
import time
# Create your views here.


def members_view(request, pk):
    council = Council.objects.select_related('chairman').get(pk = pk)
    members = [m for m in CouncilMember.objects.select_related('membership_type').filter(council__pk = pk) if council.chairman == None or  (council.chairman != None and council.chairman.pk != m.pk) ]
    gc_members = defaultdict(list)
    fc_dc_members = [m for m in members if m.membership_type.category == CouncilMembershipType.FC_DC]
    fc_members = [m for m in members if m.membership_type.category == CouncilMembershipType.FC]
    for m in [m for m in members if m.membership_type.category == CouncilMembershipType.GC]: gc_members[m.membership_type.sub_category].append(m)
    return render(request, 'legco/members.html', {'nbar': 'members', 'tbar':'legco', 'members': members, 'council': council, 'gc_members': gc_members.items(), 'fc_dc_members': fc_dc_members, 'fc_members':fc_members})

def councils_view(request):
    councils = Council.objects.all()
    return render(request, 'legco/council.html', {'nbar': 'members', 'tbar':'legco', 'councils': councils})



def individual_view(request, pk):
    individual = Individual.objects.prefetch_related('party').get(pk=pk)
    personel_ids = MeetingPersonel.objects.filter(individual__pk = pk).values('id')
    absent_total =  MeetingHansard.objects.filter(members_absent__pk__in = personel_ids).count()
    present_total =  MeetingHansard.objects.filter(members_present__pk__in = personel_ids).count()
    question_total = Question.objects.filter(individual__pk = pk).count()
    speech_total = MeetingHansard.objects.filter(speeches__individual__pk = pk).count()
    latest_speeches = MeetingHansard.objects.filter(speeches__individual__pk = pk).values_list('speeches__text_ch', 'date', 'pk', 'speeches__sequence_number').order_by('-date')[0:20]
    bill_committees = [{'title': b[0], 'id': b[1]} for b in BillCommittee.objects.filter(Q(individuals__pk__contains = pk) | Q(chairman__pk = pk) | Q(vicechairman__pk = pk)).values_list('bills_committee_title_ch', 'bill__pk').order_by('-bills_committee_formation_date')[0:10]]
    important_motions = [{'title': m[0], 'date':m[1], 'id':m[2], 'result':m[3]} for m in ImportantMotion.objects.select_related('motion').filter(motion__vote__individualvote__individual__pk = pk).values_list('motion__name_ch', 'motion__vote__date', 'motion__vote__pk', 'motion__vote__individualvote__result').order_by('-motion__vote__date')]
    return render(request, 'legco/individual.html', {'nbar': 'party', 'tbar':'legco', 'individual': individual, 'present_total': present_total, 'absent_total': absent_total, 'question_total': question_total, 'latest_speeches': latest_speeches, 'speech_total': speech_total, 'bill_committees': bill_committees, 'important_motions': important_motions})

def index_view(request):
    return render(request, 'legco/index.html', {'nbar': 'home', 'tbar':'legco'})

def speak_most_view(request):
    return render(request, 'legco/who_speaks_most.html', {'nbar': 'home', 'tbar':'legco'})

def speeches_view(request, keyword=""):
    return render(request, 'legco/speeches.html', {'nbar': 'meeting', 'tbar':'legco', 'search_keyword': keyword})

def absent_most_view(request):
    return render(request, 'legco/who_was_absent_most.html', {'nbar': 'home', 'tbar':'legco'})

def all_votes_view(request):
    return render(request, 'legco/vote.html', {'nbar': 'vote', 'tbar': 'legco'})



def truncate(s, max_length):
    return s[:max_length] + (s[max_length:] and '..')

def vote_detail(pk):
    yes_count = 0
    no_count = 0
    present_count = 0
    abstain_count = 0
    absent_count = 0
    overall_result = ""
    individual_votes = IndividualVote.objects.prefetch_related('individual').filter(vote__id = pk)
    vote = Vote.objects.prefetch_related('meeting').prefetch_related('motion').get(pk = pk)
    summaries = VoteSummary.objects.filter(vote__id = pk)
    total_count = individual_votes.count()
    for summary in summaries:
        yes_count += summary.yes_count
        no_count  += summary.no_count
        abstain_count += summary.abstain_count
        present_count += summary.present_count
        if summary.summary_type == VoteSummary.OVERALL:
            overall_result = summary.result
    absent_count = total_count - present_count
    present_vote_count = present_count - yes_count - no_count - abstain_count
    yes_individuals = [iv.individual for iv in individual_votes if iv.result == "YES"]
    no_individuals = [iv.individual for iv in individual_votes if iv.result == "NO"]
    other_individuals = [iv.individual for iv in individual_votes if iv.result not in ["YES", "NO"]]
    return overall_result, yes_count, no_count, total_count, vote, yes_individuals, no_individuals, other_individuals

def vote_detail_view(request, pk):
    vote_image_url = "https://storage.googleapis.com/g0vhk/public/legco/vote/%s.png" % (pk)
    vote = Vote.objects.prefetch_related('meeting').prefetch_related('motion').get(pk = pk)
    individual_votes = IndividualVote.objects.prefetch_related('individual').filter(vote__id = pk)
    summaries = VoteSummary.objects.filter(vote__id = pk)
    yes_count = 0
    no_count = 0
    present_count = 0
    abstain_count = 0
    absent_count = 0
    overall_result = ""
    total_count = individual_votes.count()
    for summary in summaries:
        yes_count += summary.yes_count
        no_count  += summary.no_count
        abstain_count += summary.abstain_count
        present_count += summary.present_count
        if summary.summary_type == VoteSummary.OVERALL:
            overall_result = summary.result
    absent_count = total_count - present_count
    present_vote_count = present_count - yes_count - no_count - abstain_count
    other_count = present_vote_count + absent_count + abstain_count
    meeting = MeetingHansard.objects.filter(Q(date__year = vote.date.year) & Q(date__month = vote.date.month) & Q(date__day = vote.date.day)).first()
    return render(request, 'legco/vote_detail.html', {'nbar': 'meeting', 'tbar': 'legco', 'vote': vote, 'individual_votes': individual_votes, 'summaries': summaries, 'yes_count': yes_count, 'no_count': no_count, 'abstain_count': abstain_count, 'absent_count': absent_count, 'meeting': meeting, 'overall_result': overall_result, 'present_vote_count': present_vote_count, 'pk':pk, 'og_image_url': vote_image_url, 'url': request.build_absolute_uri(), 'other_count': other_count})

def party_view(request, pk):
    party = Party.objects.get(pk = pk)
    related_news = NewsArticle.objects.filter(parties__id = pk).order_by('-date')[0:20]
    individuals = Individual.objects.filter(party__id = pk)
    return render(request, 'legco/party.html', {'party': party, 'individuals': individuals, 'nbar':'party', 'tbar': 'legco', 'related_news': related_news})

def all_parties_view(request):
    parties = Party.objects.all()
    return render(request, 'legco/all_parties.html', {'parties': parties, 'nbar': 'party', 'tbar': 'legco'})

def all_bills_view(request):
    return render(request, 'legco/bill.html', {'nbar': 'bill', 'tbar': 'legco'})

def bill_detail_view(request, pk):
    bill = Bill.objects.prefetch_related('committee').prefetch_related('first_reading').prefetch_related('second_reading').prefetch_related('third_reading').get(pk=pk)
    bill_committee_individuals = [i for i in bill.committee.individuals.all()]
    first_reading_meetings = []	 
    first_reading_dates = [bill.first_reading.first_reading_date, bill.first_reading.first_reading_date_2]
    second_reading_dates = [bill.second_reading.second_reading_date, bill.second_reading.second_reading_date_2, bill.second_reading.second_reading_date_3, bill.second_reading.second_reading_date_4, bill.second_reading.second_reading_date_5]
    third_reading_dates = [bill.third_reading.third_reading_date]
    related_meetings = MeetingHansard.objects.filter(date__in = first_reading_dates + second_reading_dates + third_reading_dates).order_by('date')
    first_reading_meetings = [meeting for meeting in related_meetings if meeting.date in [f.date() for f in first_reading_dates]]
    second_reading_meetings = [meeting for meeting in related_meetings if meeting.date in [f.date() for f in second_reading_dates]]
    third_reading_meetings = [meeting for meeting in related_meetings if meeting.date in [f.date() for f in third_reading_dates]]
    return render(request, 'legco/bill_detail.html', {'nbar': 'bill', 'tbar': 'legco', 'bill': bill, 'bill_committee_individuals': bill_committee_individuals, 
            'first_reading_meetings': first_reading_meetings,
            'second_reading_meetings': second_reading_meetings,
            'third_reading_meetings': third_reading_meetings,
        })

def all_questions_view(request, keyword=""):
    return render(request, 'legco/questions.html', {'nbar': 'question', 'tbar': 'legco', 'search_keyword': keyword})

def question_detail_view(request, pk):
    question = Question.objects.prefetch_related('individual').get(pk = pk)
    keywords = [k.keyword for k in question.keywords.all()]
    return render(request, 'legco/question_detail.html', {'nbar': 'question', 'tbar': 'legco', 'question': question, 'keywords':keywords})


def hansard_view(request, pk):
    meeting = MeetingHansard.objects.prefetch_related('speeches').prefetch_related('speeches__individual').get(pk=pk)
    present = [p for p in meeting.members_present.all()]
    absent =  [p for p in meeting.members_absent.all()]
    public = [p for p in meeting.public_officers.all()]
    clerks = [p for p in meeting.clerks.all()]
    speeches = [s for s in meeting.speeches.all() if s.title_ch != "" or s.bookmark.startswith("EV")]
    votes = Vote.objects.prefetch_related('meeting').prefetch_related('motion').filter(Q(date__year = meeting.date.year) & Q(date__month = meeting.date.month) & Q(date__day = meeting.date.day))
    for speech in speeches:
        speech.est_min = int(len(speech.text_ch) * 0.012)
        speech.text_ch_short = speech.text_ch[0:100]
        speech.text_ch_more = speech.text_ch[100:]

    return render(request, 'legco/meeting.html', {'meeting': meeting, 'speeches': speeches, 'clerks': clerks, 'public': public, 'absent': absent, 'present': present, 'nbar':'meeting', 'tbar': 'legco', 'votes':votes})


def finance_item_view(request, pk):
    item = FinanceMeetingItem.objects.get(pk=pk)
    events = FinanceMeetingItemEvent.objects.prefetch_related('vote').filter(item__pk = pk).order_by('-date')
    return render(request, 'legco/fin_item.html', {'nbar':'meeting', 'tbar': 'legco', 'item': item, 'events': events})


def fc_result_view(request, pk):
    meeting = FinanceMeetingResult.objects.get(pk=pk)
    events = FinanceMeetingItemEvent.objects.prefetch_related('vote').prefetch_related('item').filter(result__pk = meeting.id).order_by('-date')
    return render(request, 'legco/fc_result.html', {'nbar':'meeting', 'tbar': 'legco', 'events': events, 'meeting': meeting})

def open_data_view(request):
    return render(request, 'legco/opendata.html', {'nbar': 'opendata', 'tbar': 'legco'})

def meeting_view(request):
    return render(request, 'legco/meetings.html', {'nbar': 'meeting', 'tbar': 'legco'})



