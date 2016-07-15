
from django.conf.urls import url, include
from legco.views import *
urlpatterns = [
    url(r'^$', index_view),
    url(r'^vote/$', all_votes_view),
    url(r'^vote/(?P<pk>[0-9]+)/$', vote_detail_view),
    url(r'^party/(?P<pk>[0-9]+)/$', party_view),
    url(r'^party/$', all_parties_view),
    url(r'^individual/(?P<pk>[0-9]+)/$', individual_view),
    url(r'^bill/$', all_bills_view),
]


