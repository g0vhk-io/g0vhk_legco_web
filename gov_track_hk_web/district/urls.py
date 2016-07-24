from django.conf.urls import url, include
from district.views import *
urlpatterns = [
    url(r'^$', index_view)
]
