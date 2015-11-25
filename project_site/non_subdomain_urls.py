from django.conf.urls import patterns, include, url
from ddah_web.models import DDAHInstanceWeb
from django.views.generic import ListView

from django.contrib import admin
from backend import urls as backend_urls
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', ListView.as_view(
        queryset=DDAHInstanceWeb.objects.all(),
        context_object_name='instances',
        template_name='landing_page.html',
    )),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns += [
	url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^administrator/', include(backend_urls, namespace="backend")),
    url(r'^social_auth/', include('social_auth.urls')),
]
