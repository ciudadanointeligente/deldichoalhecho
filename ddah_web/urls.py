from django.conf.urls import patterns, url
from ddah_web.views import DDAHInstanceWebView

urlpatterns = patterns('',
        url(r'^$',
            DDAHInstanceWebView.as_view(),
            name='instance_home'),
)
