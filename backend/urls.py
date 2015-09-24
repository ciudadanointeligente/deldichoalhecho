from django.conf.urls import patterns, url
from ddah_web.views import DDAHInstanceWebView, DDAHInstanceWebJSONView, FlatPageView
from django.http import HttpResponse
from .views import BackendHomeView


urlpatterns = patterns('',
    url(r'^hola/?$', BackendHomeView.as_view(), name='home'),
)
