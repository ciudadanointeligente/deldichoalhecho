from django.conf.urls import patterns, include, url
from django.contrib import admin
from promises_web.views import HomeView
admin.autodiscover()

urlpatterns = patterns('',
        url(r'^(?P<label>[-\w]+)/?$', 
        	HomeView.as_view(template_name='home.html',), 
        	name = 'instance_home'),
)
