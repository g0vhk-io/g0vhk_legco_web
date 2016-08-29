from django.conf.urls import url
from views import ConsultationsFeed, NewsFeed

urlpatterns = [
    # ...
    url(r'^consultations.xml$', ConsultationsFeed()),
    url(r'^news.xml$', NewsFeed()),
    # ...
]

