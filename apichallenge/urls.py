from django.contrib import admin
from django.conf.urls import url,include
from urlshortner.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'',include('urlshortner.urls')),
]