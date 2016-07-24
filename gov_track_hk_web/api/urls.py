from django.conf.urls import url, include
from rest_framework import routers
from api import views
router = routers.DefaultRouter()
router.register(r'latest_bills', views.LatestBillsViewSet, base_name='latest_bills')
router.register(r'latest_votes', views.LatestVotesViewSet, base_name='latest_votes')
router.register(r'votes_search/(?P<keyword>.*)', views.VotesSearchViewSet, base_name='votes_search')
router.register(r'parties', views.PartiesViewSet)
router.register(r'meetings', views.MeetingsViewSet, base_name='meetings')
router.register(r'questions', views.LatestQuestionsViewSet, base_name='questions')
router.register(r'most_absent', views.MostAbsentViewSet, base_name='most_absent')
router.register(r'consultations', views.ConsultationsViewSet, base_name='consultations')
router.register(r'party/(?P<pk>.+)', views.PartyDetailViewSet, base_name='party')
router.register(r'bills_search/(?P<keyword>.*)', views.BillsSearchViewSet, base_name='bills_search')
urlpatterns = [
    url(r'', include(router.urls))
]


