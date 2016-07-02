from django.conf.urls import url, include
from rest_framework import routers
from api import views
router = routers.DefaultRouter()
router.register(r'latest_votes', views.LatestVotesViewSet)
router.register(r'parties', views.PartiesViewSet)
urlpatterns = [
    url(r'', include(router.urls))
]


