from django.conf.urls import patterns, url
from ddah_web.views import DDAHInstanceWebView, DDAHInstanceWebJSONView

urlpatterns = patterns('',
        url(r'^data.json$',
            DDAHInstanceWebJSONView.as_view(),
            name='data_json'),
        url(r'^$',
            DDAHInstanceWebView.as_view(),
            name='instance_home'),
)
