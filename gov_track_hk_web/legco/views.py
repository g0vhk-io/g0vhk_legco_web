from django.shortcuts import render
from legco.models import Individual, Party
# Create your views here.


def index_view(request):
    return render(request, 'legco/index.html', {'nbar': 'home'})

def vote_view(request):
    return render(request, 'legco/vote.html', {'nbar': 'vote'})


def party_view(request, pk):
    party = Party.objects.get(pk = pk)
    individuals = Individual.objects.filter(party__id = pk)
    return render(request, 'legco/party.html', {'party': party, 'individuals': individuals, 'nbar':'party'})

def all_parties_view(request):
    parties = Party.objects.all()
    return render(request, 'legco/all_parties.html', {'parties': parties, 'nbar': 'party'})
