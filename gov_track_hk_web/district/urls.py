from django.conf.urls import url

from district.views import index_view

urlpatterns = [
    url(r'^$', index_view)
]
