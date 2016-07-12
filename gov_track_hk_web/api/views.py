from django.core.cache import cache
from rest_framework import viewsets
from django.db.models import Count
from legco.models import Vote, Motion, Party, Individual, IndividualVote, VoteSummary
from rest_framework import serializers
from rest_framework.response import Response
from gov_track_hk_web.settings import MORPH_IO_API_KEY
import requests

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
