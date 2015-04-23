from django.conf.urls import patterns, url
from ddah_web.views import DDAHInstanceWebView

urlpatterns = patterns('',
        url(r'^(?P<slug>[-\w]+)/?$',
            DDAHInstanceWebView.as_view(),
            name='instance_home'),
)
