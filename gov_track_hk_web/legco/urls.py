
from django.conf.urls import url, include
from legco.views import *
urlpatterns = [
    url(r'^$', index_view),
    url(r'^vote/$', vote_view),
    url(r'^party/(?P<pk>[0-9]+)/$', party_view),
    url(r'^party/$', all_parties_view)

]


