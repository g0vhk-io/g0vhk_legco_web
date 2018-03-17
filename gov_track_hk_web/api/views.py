# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.db.models import Q
from django.core.cache import cache
from rest_framework import viewsets
from django.db.models import Count
from legco.models import Vote, Motion, Party, Individual, IndividualVote, VoteSummary, Bill, Question, MeetingHansard, MeetingSpeech, ImportantMotion, ImportantMotion
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from datetime import datetime, timedelta, date
from subscriber.models import Subscriber, News
from hashlib import md5
import requests
from lxml import etree, html
import re
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from api.models import Consultation



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

class MostPresentIndividualsViewSet(viewsets.ViewSet):
    def  list(self, request):
        size = int(request.query_params.get("size", size))
        query = MeetingHansard.objects.filter(date__gt=date(2016, 9, 10))
        present_total =  query.values('members_present__individual__pk', 'members_present__individual__name_ch').annotate(dcount=Count('members_present__individual__pk')).order_by('-dcount')
        result = []
        for d in present_total:
            pk = d['members_present__individual__pk']
            name_ch = d['members_present__individual__name_ch']
            dcount = d['dcount']
            result.append({'id': pk, 'name': name_ch, 'total': dcount})
        return Response(result[0:size])

class MostSpeechIndividualsViewSet(viewsets.ViewSet):
    def  list(self, request):
        size = int(request.query_params.get("size", 5))
        query = MeetingSpeech.objects.filter(meetinghansard__date__gt=date(2016, 9, 10))
        speech_total =  query.values('individual__pk', 'individual__name_ch', 'individual__image').annotate(dcount=Count('individual__pk')).order_by('-dcount')
        result = []
        m = max([d['dcount'] for d in speech_total])
        for d in speech_total:
            pk = d['individual__pk']
            name_ch = d['individual__name_ch']
            dcount = d['dcount']
            image = d['individual__image']
            result.append({'id': pk, 'name': name_ch, 'total': dcount, 'max': m, 'image': image})
        return Response(result[0:size])


class MostAbsentIndividualsViewSet(viewsets.ViewSet):
    def  list(self, request):
        size = int(request.query_params.get("size", 5))
        query = MeetingHansard.objects.filter(date__gt=date(2016, 9, 10))
        meeting_total = query.count()
        absent_total =  query.all() \
        .values('members_absent__individual__pk', 'members_absent__individual__name_ch', 'members_absent__individual__image') \
        .annotate(dcount=Count('members_absent__individual__pk')).order_by('-dcount')
        result = []
        for d in absent_total:
            pk = d['members_absent__individual__pk']
            name_ch = d['members_absent__individual__name_ch']
            image = d['members_absent__individual__image']
            dcount = d['dcount']
            if pk is None:
                continue
            result.append({'id': pk, 'name': name_ch, 'total': dcount, 'image': image, 'max': meeting_total})
        return Response(result[0:size])



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

class AllBillsViewSet(viewsets.ViewSet):
    def list(self, request, keyword=""):
        page = int(request.query_params.get("page", "1")) - 1
        if page < 0:
            page = 0
        page_size = 50
        bills = Bill.objects.filter(Q(committee__bills_committee_title_ch__contains = keyword)| Q(bill_title_ch__contains = keyword)| Q(description__contains = keyword))
        output = []
        total = bills.count()
        for bill in bills[page_size * page: (page + 1) * page_size]:
            output.append({'title_en': bill.bill_title_en, 'title_ch': bill.bill_title_ch, 'id': bill.id, 'passed': len(bill.ordinance_gazette_content_url_ch) > 0, 'content': bill.ordinance_gazette_content_url_ch, 'ordinance_title_ch': bill.ordinance_title_ch, 'proposer_ch': bill.proposed_by_ch})
        return Response({'data':output, 'keyword': keyword, 'page':page + 1, 'total': total, 'page_size': page_size})

class MeetingSpeechSearchViewSet(viewsets.ViewSet):
    def list(self, request, keyword=""):
        page = int(request.query_params.get("page", "1")) - 1
        if page < 0:
            page = 0
        page_size = 50
        speeches = MeetingSpeech.objects.prefetch_related('individual').filter(~Q(title_ch = "")&(Q(title_ch__contains = keyword) | Q(text_ch__contains = keyword))).values_list('text_ch', 'title_ch', 'sequence_number', 'individual__id','individual__name_ch','individual__image', 'meetinghansard__id', 'meetinghansard__date').order_by('-meetinghansard__date')

        total = speeches.count()
        output = []
        for l in speeches[page_size * page: (page + 1) * page_size]:
            text, title, seq_num, individual_id, individual_name, individual_image, meeting_id, meeting_date = l
            i_dict = None
            m_dict = {'date': meeting_date, 'id': meeting_id}
            if meeting_id is None:
                continue
            if individual_id is not None:
                i_dict = {'id': individual_id, 'name_ch': individual_name, 'image': individual_image}
            p = text.find(keyword)
            pre_text_short = ".."
            post_text_short = ".."
            start = p - 10
            if start < 0:
                start = 0
                pre_text_short = ""
            end = start + 50
            l = len(text)
            if end > l :
                end = l - 1
                post_text_short = ""
            short_text = pre_text_short + text[start:end] + post_text_short
            output.append({'text_short_ch': short_text, 'title_ch': title, 'individual': i_dict, 'seq_num': seq_num, 'meeting': m_dict})
        return Response({'data':output, 'keyword': keyword, 'page':page + 1, 'total': total, 'page_size': page_size})


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

class ConsultationsViewSet(viewsets.ViewSet):
    def list(self, request):
        now = datetime.now()
        earlier = now - timedelta(days=30)
        consultations = Consultation.objects.filter(Q(lang = "tc") & Q(date__gte=earlier))
        items = [{'date': c.date, 'link': c.link, 'title': c.title, 'lang': c.lang} for c in consultations]
        items = sorted(items, key=lambda item: item['date'], reverse=True)
        return Response(items)

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
            lines = "\n".join([s.strip() for s in html_root.xpath("//p/text()")]).split("\n")
            lines = [l.strip() for l in lines]
            temperature, humidity = [int(re.match('[^\d]*(\d+).*', s).group(1)) for s in lines[3:5]]
            item = {'temperature': temperature, 'humidity': humidity, 'image': img}
            cache.set(key, item,  60 * 60)
            cached_json = item
        return Response(cached_json)

class LatestQuestionsViewSet(viewsets.ViewSet):
    def list(self, request, keyword=""):
        page = int(request.query_params.get("page", "1")) - 1
        if page < 0:
            page = 0
        page_size = 50
        questions = Question.objects.filter(Q(question__contains = keyword)| Q(answer__contains = keyword)).prefetch_related('individual').prefetch_related('keywords').order_by('-date')
        total = questions.count()
        return Response({'data':[{'id': q.id, 'date': q.date.strftime('%Y-%m-%d'), 'question_type': q.question_type, 'question': q.question[0:100] + "...", 'answer': q.answer[0:100] + "...", 'title': q.title_ch, 'individual':{'name': q.individual.name_ch, 'id':q.individual.id, 'image': q.individual.image}, 'keywords': [k.keyword for k in q.keywords.all()]} for q in questions[page_size * page: (page + 1) * page_size]], 'total':total, 'page_size': page_size, 'page': page + 1, 'keyword': keyword})


class ImportantMotionViewSet(viewsets.ViewSet):
    def list(self, request):
        data = []
        motions = ImportantMotion.objects.select_related('motion').values_list('motion__name_ch', 'motion__vote__date', 'motion__vote__pk').order_by('-motion__vote__date')
        summaries = VoteSummary.objects.filter(Q(vote__pk__in = [m[2] for m in motions]) & Q(summary_type = VoteSummary.OVERALL))
        result_dict = {s.vote_id: s.result for s in summaries}
        for motion in motions:
            data.append({'title_ch': motion[0], 'date': motion[1], 'id': motion[2], 'result': result_dict[motion[2]]})
        return Response({'data':data})

class MeetingsViewSet(viewsets.ViewSet):
    def list(self, request, year="2015"):
        year = int(year)
        meetings = MeetingHansard.objects.filter(Q(Q(date__year = year + 1) & Q(date__month__lt = 9)) | ( Q(date__year = year)& Q(date__month__gte = 9))).order_by('-date')
        result = []
        for m in meetings:
            present = [p for p in m.members_present.all()]
            absent =  [p for p in m.members_absent.all()]
            votes = Vote.objects.prefetch_related('meeting').prefetch_related('motion').filter(Q(date__year = m.date.year) & Q(date__month = m.date.month) & Q(date__day = m.date.day))

            result.append({'id': m.id, 'date': m.date.strftime('%Y-%m-%d'), 'type': m.meeting_type,
                'present_count': len(present),
                'absent_count': len(absent),
                'vote_count': len(votes)})

        return Response(result)

class NewsViewSet(viewsets.ViewSet):
    def list(self, request):
        news = News.objects.all().order_by('-date')[0:10]  
        result = [{'title_ch': n.title_ch, 'text_ch': n.text_ch, 'date': n.date.strftime('%Y-%m-%d')} for n in news]
        return Response(result)



class SubscribeViewSet(viewsets.ViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def create(self, request):
        subscriber = Subscriber()
        subscriber.email = request.data['email']
        m = md5()
        m.update(subscriber.email)
        subscriber.key = str(m.hexdigest())
        try:
            subscriber.save()
            return Response({"status": "ok"})
        except IntegrityError:
            return Response({"status": "already"})
