from django.conf.urls import patterns, url
from ddah_web.views import DDAHInstanceWebView, DDAHInstanceWebJSONView, FlatPageView
from django.http import HttpResponse
from .views import BackendHomeView, InstanceDetailView, CSVUploadView


urlpatterns = patterns('',
    url(r'^/?$', BackendHomeView.as_view(), name='home'),
    url(r'^detail/(?P<slug>[\w-]+)/?$', InstanceDetailView.as_view(), name='instance'),
    url(r'^detail/(?P<slug>[\w-]+)/upload/?$', CSVUploadView.as_view(), name='csv_upload'),
)
