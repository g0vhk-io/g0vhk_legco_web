from django.shortcuts import render
# Create your views here.


def index_view(request):
    return render(request, 'index.html', {'tbar': 'home', 'nbar':'home'})

def other_projects_view(request):
    return render(request, 'other_projects.html', {'tbar': 'home', 'nbar':'projects'})


