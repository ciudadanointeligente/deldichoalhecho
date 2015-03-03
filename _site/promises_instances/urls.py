from django.conf.urls import patterns, include, url
from django.contrib import admin
from promises_web.views import HomeView
from promises_instances.views import InstanceDetailView

urlpatterns = patterns('',
        url(r'^(?P<slug>[-\w]+)/?$', 
            InstanceDetailView.as_view(template_name='home.html',), 
            name = 'instance_home'),
)
