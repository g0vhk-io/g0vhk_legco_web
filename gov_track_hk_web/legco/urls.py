
from django.conf.urls import url, include
from legco.views import *
urlpatterns = [
    url(r'^$', index_view),
    url(r'^vote/$', all_votes_view),
    url(r'^vote/(?P<pk>[0-9]+)/$', vote_detail_view),
    url(r'^party/(?P<pk>[0-9]+)/$', party_view),
    url(r'^party/$', all_parties_view),
    url(r'^individual/(?P<pk>[0-9]+)/$', individual_view),
    url(r'^question/(?P<pk>[0-9]+)/$', question_detail_view),
    url(r'^bill/(?P<pk>[0-9]+)/$', bill_detail_view),
    url(r'^bill/$', all_bills_view),
    url(r'^question/$', all_questions_view),
    url(r'^meeting/(?P<pk>[0-9]+)/$', hansard_view),
    url(r'^fin_item/(?P<pk>[0-9]+)/$', finance_item_view),
    url(r'^fc_result/(?P<pk>[0-9]+)/$', fc_result_view),
    url(r'^opendata/$', open_data_view),
    url(r'^meeting/$', meeting_view)
]


