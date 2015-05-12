from django.conf.urls import patterns, include, url
from ddah_web.models import DDAHInstanceWeb
from django.views.generic import ListView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', ListView.as_view(
        queryset=DDAHInstanceWeb.objects.all(),
        context_object_name='instances',
        template_name='landing_page.html',
    )),
    url(r'^admin/', include(admin.site.urls)),
)


# Your other patterns here
urlpatterns += [
    url(r'^pages/', include('django.contrib.flatpages.urls')),
]
