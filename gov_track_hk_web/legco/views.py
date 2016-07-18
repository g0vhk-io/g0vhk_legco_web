from django.shortcuts import render
from django.db.models import Count
from legco.models import Individual, Party, NewsArticle, IndividualVote, Vote, VoteSummary, Bill
# Create your views here.


def individual_view(request, pk):
    individual = Individual.objects.prefetch_related('party').get(pk=pk)
    related_news = NewsArticle.objects.filter(individuals__id = pk)[0:20]
    frequency = IndividualVote.objects.filter(individual__pk = pk).values('result').annotate(dcount=Count('result')).order_by('-dcount')
    related_votes = IndividualVote.objects.prefetch_related('vote').prefetch_related('vote__motion').filter(individual__pk = pk).order_by('-vote__date')[0:20]
    return render(request, 'legco/individual.html', {'nbar': 'home', 'tbar':'legco', 'individual': individual, 'related_news': related_news, 'related_votes': related_votes, 'frequency': frequency})

def index_view(request):
    return render(request, 'legco/index.html', {'nbar': 'home', 'tbar':'legco'})

def all_votes_view(request):
    return render(request, 'legco/vote.html', {'nbar': 'vote', 'tbar': 'legco'})

def vote_detail_view(request, pk):
    vote = Vote.objects.prefetch_related('meeting').prefetch_related('motion').get(pk = pk)
    individual_votes = IndividualVote.objects.prefetch_related('individual').filter(vote__id = pk)
    summaries = VoteSummary.objects.filter(vote__id = pk)
    yes_count = 0
    no_count = 0
    present_count = 0
    for summary in summaries:
        yes_count += summary.yes_count
        no_count  += summary.no_count
        present_count += summary.yes_count + summary.no_count + summary.abstain_count
    abstain_count = len(individual_votes) - yes_count - no_count - 1
    return render(request, 'legco/vote_detail.html', {'nbar': 'vote', 'tbar': 'legco', 'vote': vote, 'individual_votes': individual_votes, 'summaries': summaries, 'yes_count': yes_count, 'no_count': no_count, 'abstain_count': abstain_count})

def party_view(request, pk):
    party = Party.objects.get(pk = pk)
    related_news = NewsArticle.objects.filter(parties__id = pk)[0:20]
    individuals = Individual.objects.filter(party__id = pk)
    return render(request, 'legco/party.html', {'party': party, 'individuals': individuals, 'nbar':'party', 'tbar': 'legco', 'related_news': related_news})

def all_parties_view(request):
    parties = Party.objects.all()
    return render(request, 'legco/all_parties.html', {'parties': parties, 'nbar': 'party', 'tbar': 'legco'})

def all_bills_view(request):
    return render(request, 'legco/bill.html', {'nbar': 'bill', 'tbar': 'legco'})

def bill_detail_view(request, pk):
    bill = Bill.objects.prefetch_related('committee').prefetch_related('first_reading').prefetch_related('second_reading').prefetch_related('third_reading').get(pk=pk)
    return render(request, 'legco/bill_detail.html', {'nbar': 'bill', 'tbar': 'legco', 'bill': bill})
