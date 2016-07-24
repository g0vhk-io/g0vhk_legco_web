from django.shortcuts import render
from django.db.models import Count
def index_view(request):
    return render(request, 'district/index.html', {'nbar': 'home', 'tbar':'dc'})

