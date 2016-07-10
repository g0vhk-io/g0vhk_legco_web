from django.conf.urls import url, include
from rest_framework import routers
from api import views
router = routers.DefaultRouter()
router.register(r'latest_votes', views.LatestVotesViewSet, base_name='latest_votes')
router.register(r'parties', views.PartiesViewSet)
router.register(r'most_absent', views.MostAbsentViewSet, base_name='most_absent')
router.register(r'consultations', views.ConsultationsViewSet, base_name='consultations')
router.register(r'party/(?P<pk>.+)', views.PartyDetailViewSet, base_name='party')
urlpatterns = [
    url(r'', include(router.urls))
]


