from django.shortcuts import render
from legco.models import Individual, Party, NewsArticle, IndividualVote
# Create your views here.


def individual_view(request, pk):
    individual = Individual.objects.prefetch_related('party').get(pk=pk)
    related_news = NewsArticle.objects.filter(individuals__id = pk)[0:20]
    related_votes = IndividualVote.objects.prefetch_related('vote').prefetch_related('vote__motion').filter(individual__pk = pk).order_by('-vote__date')[0:20]
    return render(request, 'legco/individual.html', {'nbar': 'home', 'tbar':'legco', 'individual': individual, 'related_news': related_news, 'related_votes': related_votes})

def index_view(request):
    return render(request, 'legco/index.html', {'nbar': 'home', 'tbar':'legco'})

def vote_view(request):
    return render(request, 'legco/vote.html', {'nbar': 'vote', 'tbar': 'legco'})


def party_view(request, pk):
    party = Party.objects.get(pk = pk)
    individuals = Individual.objects.filter(party__id = pk)
    return render(request, 'legco/party.html', {'party': party, 'individuals': individuals, 'nbar':'party', 'tbar': 'legco'})

def all_parties_view(request):
    parties = Party.objects.all()
    return render(request, 'legco/all_parties.html', {'parties': parties, 'nbar': 'party', 'tbar': 'legco'})
