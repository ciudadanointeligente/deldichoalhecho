from django.conf.urls import patterns, url
from ddah_web.views import DDAHInstanceWebView, DDAHInstanceWebJSONView, FlatPageView
from django.http import HttpResponse
from .views import BackendHomeView, InstanceDetailView, CSVUploadView, StyleView, CategoryCreateView


urlpatterns = patterns('',
    url(r'^/?$', BackendHomeView.as_view(), name='home'),
    url(r'^detail/(?P<slug>[\w-]+)/?$', InstanceDetailView.as_view(), name='instance'),
    url(r'^detail/(?P<slug>[\w-]+)/style/?$', StyleView.as_view(), name='instance_style'),
    url(r'^detail/(?P<slug>[\w-]+)/category_create/?$', CategoryCreateView.as_view(), name='create_category'),
    url(r'^detail/(?P<slug>[\w-]+)/upload/?$', CSVUploadView.as_view(), name='csv_upload'),
)
