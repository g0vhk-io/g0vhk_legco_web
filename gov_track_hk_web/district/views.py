from django.shortcuts import render


def index_view(request):
    return render(request,
                  'district/index.html',
                  {'nbar': 'home', 'tbar': 'dc'})
