
from django.conf.urls import url, include
from legco.views import index_view
urlpatterns = [
    url(r'', index_view)


]


