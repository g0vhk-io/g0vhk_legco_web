from django.conf.urls import url, include
from rest_framework import routers
from api import views
router = routers.DefaultRouter()
router.register(r'latest_bills', views.LatestBillsViewSet, base_name='latest_bills')
router.register(r'latest_votes', views.LatestVotesViewSet, base_name='latest_votes')
router.register(r'votes_search/(?P<keyword>.*)', views.VotesSearchViewSet, base_name='votes_search')
router.register(r'parties', views.PartiesViewSet)
router.register(r'meetings', views.MeetingsViewSet, base_name='meetings')
router.register(r'meetings/(?P<year>[0-9]+)', views.MeetingsViewSet, base_name='meetings')
router.register(r'questions', views.LatestQuestionsViewSet, base_name='questions')
router.register(r'questions/(?P<keyword>\w*)', views.LatestQuestionsViewSet, base_name='questions')
router.register(r'questions/(?P<keyword>\w*)/(?P<page>[0-9]+)', views.LatestQuestionsViewSet, base_name='questions')
router.register(r'most_present', views.MostPresentIndividualsViewSet, base_name='most_present')
router.register(r'most_absent', views.MostAbsentIndividualsViewSet, base_name='most_absent')
router.register(r'most_speech', views.MostSpeechIndividualsViewSet, base_name='most_speech')
router.register(r'subscribe', views.SubscribeViewSet, base_name='subscribe')
router.register(r'consultations', views.ConsultationsViewSet, base_name='consultations')
router.register(r'weather', views.WeatherViewSet, base_name='weather')
router.register(r'party/(?P<pk>.+)', views.PartyDetailViewSet, base_name='party')
router.register(r'bills', views.AllBillsViewSet, base_name='bills')
router.register(r'bills/(?P<keyword>\w*)', views.AllBillsViewSet, base_name='bills')
router.register(r'bills/(?P<keyword>\w*)/(?P<page>[0-9]+)', views.AllBillsViewSet, base_name='bills')
router.register(r'important_motion', views.ImportantMotionViewSet, base_name='important_motion')
urlpatterns = [
    url(r'', include(router.urls))
]


