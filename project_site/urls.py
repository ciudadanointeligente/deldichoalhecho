from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('ddah_web.urls')),
)


# Your other patterns here
urlpatterns += [
    url(r'^pages/', include('django.contrib.flatpages.urls')),
]
