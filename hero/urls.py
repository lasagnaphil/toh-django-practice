from django.conf.urls import url, include
from .views import heroList, heroDetail

urlpatterns = [
    url(r'^hero$', heroList, name='heroList'),
    url(r'^hero/(?P<hero_id>[0-9]+)$', heroDetail, name='heroDetail'),
]
