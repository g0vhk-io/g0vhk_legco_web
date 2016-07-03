from rest_framework import viewsets
from django.db.models import Count
from legco.models import Vote, Motion, Party, Individual, IndividualVote
from rest_framework import serializers
from rest_framework.response import Response

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


class LatestVotesViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.order_by('-date', '-time')[0:20]
    serializer_class = VoteSerializer


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
