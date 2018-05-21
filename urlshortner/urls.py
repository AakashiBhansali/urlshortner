from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^fetch/short-url/$', CreateShortURL, name='create-short-url'),
    url(r'^fetch/long-url/$', FetchLongURL, name='fetch-long-url'),
    url(r'^fetch/short-urls/$', CreateShortURLs, name='create-short-urls'),
    url(r'^fetch/long-urls/$', FetchLongURLs, name='fetch-long-urls'),
    url(r'^fetch/count/$', FetchCount, name='fetch-count'),
    url(r'^clean-urls/$', CleanURL, name='clean-url'),
    url(r'^(?P<short_url_hash>[\w-]+)/$', RedirectURL, name='redirect-url'),
]
