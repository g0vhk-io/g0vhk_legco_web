# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.db.models import Q
from django.core.cache import cache
from rest_framework import viewsets
from django.db.models import Count
from legco.models import Vote, Motion, Party, Individual, IndividualVote, VoteSummary, Bill, Question, MeetingHansard
from rest_framework import serializers
from rest_framework.response import Response
from gov_track_hk_web.settings import MORPH_IO_API_KEY
from rest_framework.decorators import detail_route, list_route
from datetime import datetime
from subscriber.models import Subscriber
import md5
import requests
from lxml import etree, html
import re
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class MotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Motion
        fields = ('name_en', 'name_ch', 'mover_type', 'mover_ch', 'mover_en')

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    motion = MotionSerializer(many=False)
    class Meta:
        model = Vote
        fields = ('date', 'time', 'motion', 'vote_number')

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields =  ('name_ch', 'name_en', 'id')

class IndividiualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Individual
        fields =  ('name_en', 'name_ch', 'id')


class LatestVotesViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Vote.objects.all().prefetch_related('motion').order_by('-date', '-time')[:20]
        pks = [i.id for i in queryset]
        summaries = VoteSummary.objects.filter(vote__pk__in = pks)
        summary_dict = {}
        for summary in summaries:
            if summary.vote.id not in summary_dict:
                summary_dict[summary.vote.id] = []
            summary_dict[summary.vote.id].append(
            {'summary_type': summary.summary_type,
             'present_count':summary.present_count,
             'yes_count':summary.yes_count,
             'no_count':summary.no_count,
             'abstain_count':summary.abstain_count,
             'vote_count': summary.vote_count,
             'result': summary.result
            })
        results = [{'date': q.date, 'time': q.time, 'id': q.id, 'motion': {'name_ch': q.motion.name_ch, 'mover_ch': q.motion.mover_ch},'summaries':summary_dict[q.id]} for q in queryset]
        return Response(results)

class VotesSearchViewSet(viewsets.ViewSet):
    def list(self, request, keyword):
        queryset = Vote.objects.all().prefetch_related('motion').filter(Q(motion__name_ch__contains = keyword) | Q(motion__mover_ch__contains = keyword)).order_by('-date', '-time')[0:100]
        pks = [i.id for i in queryset]
        summaries = VoteSummary.objects.filter(vote__pk__in = pks)
        summary_dict = {}
        for summary in summaries:
            if summary.vote.id not in summary_dict:
                summary_dict[summary.vote.id] = []
            summary_dict[summary.vote.id].append(
            {'summary_type': summary.summary_type,
             'present_count':summary.present_count,
             'yes_count':summary.yes_count,
             'no_count':summary.no_count,
             'abstain_count':summary.abstain_count,
             'vote_count': summary.vote_count,
             'result': summary.result
            })
        results = [{'date': q.date, 'time': q.time, 'id': q.id, 'motion': {'name_ch': q.motion.name_ch, 'mover_ch': q.motion.mover_ch},'summaries':summary_dict[q.id]} for q in queryset]
        return Response(results)

class BillsSearchViewSet(viewsets.ViewSet):
    def list(self, request, keyword):
        queryset = Bill.objects.all().prefetch_related('committee').prefetch_related('first_reading').prefetch_related('second_reading').prefetch_related('third_reading').filter(bill_title_ch__contains = keyword).order_by('-committee__bills_committee_formation_date')[0:100]
        pks = [i.id for i in queryset]
        results = [{'id': q.id, 'title': q.bill_title_ch, 'committee': q.committee.bills_committee_title_ch, 'ordinance': q.ordinance_title_ch} for q in queryset]
        return Response(results)


class LatestBillsViewSet(viewsets.ViewSet):
    def list(self, request):
        bills = Bill.objects.filter(third_reading__third_reading_date = datetime.min)
        output = []
        for bill in bills:
            output.append({'title_en': bill.bill_title_en, 'title_ch': bill.bill_title_ch, 'id': bill.id})
        return Response(output)


class PartiesViewSet(viewsets.ModelViewSet):
    queryset = Party.objects.all()
    serializer_class = PartySerializer

class PartyDetailViewSet(viewsets.ViewSet):
    def list(self, request, pk=1):
        queryset = Party.objects.get(pk = pk)
        party_serializer = PartySerializer(queryset)
        individuals = Individual.objects.filter(party__id = pk)
        individual_serializers = [ IndividiualSerializer(i) for i in individuals]
        return Response({'party': party_serializer.data, 'individuals': [i.data for i in individual_serializers]})

class MostAbsentViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = IndividualVote.objects.filter(result=IndividualVote.ABSENT).values('individual__name_ch', 'individual__pk').annotate(dcount=Count('individual__name_ch')).order_by('-dcount')[:5]
        result = [{'count': d['dcount'], 'individual': {'name': d['individual__name_ch'], 'id':d['individual__pk']} } for d in queryset]
        return Response(result)

class ConsultationsViewSet(viewsets.ViewSet):
    def list(self, request):
        key = "consultations_json"
        cached_json = cache.get(key)
        if cached_json is None:
            url = "https://api.morph.io/howawong/hong_kong_current_consultation_pages/data.json?key=%s&query=select%%20*%%20from%%20'data'%%20limit%%20100" % (MORPH_IO_API_KEY)
            r = requests.get(url)
            items = [r for r in  r.json() if r['lang'] == 'tc']
            items = sorted(items, key=lambda item: item['date'], reverse=True)
            cache.set(key, items, 24 * 60 * 60)
            cached_json = items
        return Response(cached_json)

class WeatherViewSet(viewsets.ViewSet):
    def list(self, request):
        key = "weather_json"
        cached_json = cache.get(key)
        if cached_json is None:
            url = "http://rss.weather.gov.hk/rss/CurrentWeather.xml"
            feed = requests.get(url)
            root = etree.fromstring(feed.content)
            summary = root.xpath("//description")[1]
            html_root =  html.fromstring(summary.text)
            img = html_root.xpath("//img/@src")[0].strip()
            print "image url [%s]" % img
            lines = "\n".join([s.strip() for s in html_root.xpath("//p/text()")]).split("\n")
            lines = [l.strip() for l in lines]
            temperature, humidity = [int(re.match('[^\d]*(\d+).*', s).group(1)) for s in lines[3:5]]
            item = {'temperature': temperature, 'humidity': humidity, 'image': img}
            cache.set(key, item,  60 * 60)
            cached_json = item
        return Response(cached_json)

class LatestQuestionsViewSet(viewsets.ViewSet):
    def list(self, request):
        questions = Question.objects.all().prefetch_related('individual').prefetch_related('keywords').order_by('-date')[0:50]
        return Response([{'id': q.id, 'date': q.date.strftime('%Y-%m-%d'), 'question_type': q.question_type, 'question': q.question[0:100] + "...", 'answer': q.answer[0:100] + "...", 'title': q.title_ch, 'individual':{'name': q.individual.name_ch, 'id':q.individual.id, 'image': q.individual.image}, 'keywords': [k.keyword for k in q.keywords.all()]} for q in questions])


class MeetingsViewSet(viewsets.ViewSet):
    def list(self, request):
        meetings = MeetingHansard.objects.all().order_by('-date')[0:50]
        return Response([{'id': m.id, 'date': m.date.strftime('%Y-%m-%d'), 'type': m.meeting_type} for m in meetings])

class SubscribeViewSet(viewsets.ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def create(self, request):
        subscriber = Subscriber()
        subscriber.email = request.data['email']
        subscriber.key = str(md5.new(subscriber.email).hexdigest())
        try:
            subscriber.save()
            return Response({"status": "ok"})
        except IntegrityError:
            return Response({"status": "already"})
