from django.conf.urls import patterns, url
from .views import BackendHomeView, InstanceDetailView, CSVUploadView, StyleView, CategoryCreateView, PromiseCreateView, PromiseUpdateView


urlpatterns = patterns('',
    url(r'^/?$', BackendHomeView.as_view(), name='home'),
    url(r'^detail/(?P<slug>[\w-]+)/?$', InstanceDetailView.as_view(), name='instance'),
    url(r'^detail/(?P<slug>[\w-]+)/category_create/?$', CategoryCreateView.as_view(), name='create_category'),
    url(r'^detail/(?P<label>[\w-]+)/(?P<category_id>[\w-]+)/promise_create/?$', PromiseCreateView.as_view(), name='create_promise'),
    url(r'^detail/(?P<pk>[\d-]+)/promise_update/?$', PromiseUpdateView.as_view(), name='update_promise'),
    url(r'^detail/(?P<slug>[\w-]+)/style/?$', StyleView.as_view(), name='instance_style'),
    url(r'^detail/(?P<slug>[\w-]+)/upload/?$', CSVUploadView.as_view(), name='csv_upload'),
)
