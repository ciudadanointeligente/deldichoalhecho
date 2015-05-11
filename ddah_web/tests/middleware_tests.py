from django.test import TestCase, RequestFactory, override_settings
from django.contrib.sites.models import Site
from promises_instances.models import DDAHInstance
from ddah_web.models import DDAHSiteInstance, DDAHInstanceWeb
from ddah_web.middleware import DDAHSiteMiddleware
from django.http.request import HttpRequest
from django.core.urlresolvers import reverse
from ddah_web.views import DDAHInstanceWebView


class InstanceSiteRelationTestCase(TestCase):
    def setUp(self):
        pass

    def test_create_an_instance(self):
        the_site = Site.objects.create(name="name", domain="www.the_site.com")
        instance = DDAHInstanceWeb.objects.create(label="bici", title="Bicicletas")
        the_record = DDAHSiteInstance.objects.create(site=the_site, instance=instance)
        self.assertTrue(the_record)
        self.assertEquals(the_record.site, the_site)
        self.assertEquals(the_record.instance, instance)
        self.assertIn(the_site.domain, the_record.__unicode__())
        self.assertIn(instance.title, the_record.__unicode__())


@override_settings(ALLOWED_HOSTS=['*'])
class DDAHMiddlewareTestCase(TestCase):
    '''
    This middleware gets the request and decides if there is an instance matching this request.
    The  subdomains.middleware should go first and this middleware should only decide if subdomain
    hasn't set the instance first.
    '''

    def setUp(self):
        self.the_site = Site.objects.create(name="name", domain="the-site.com")
        self.instance = DDAHInstanceWeb.objects.create(label="bici", title="Bicicletas")
        self.the_record = DDAHSiteInstance.objects.create(site=self.the_site, instance=self.instance)
        self.factory = RequestFactory()

    def test_site_is_set_and_related_to_an_instance(self):
        request = self.factory.get('/')
        request.META['SERVER_NAME'] = self.the_site.domain
        middleware = DDAHSiteMiddleware()

        middleware.process_request(request)
        self.assertEquals(request.instance, self.instance)

    def test_instance_is_set_returns_itself(self):
        request = self.factory.get('/')
        request.instance = self.instance
        middleware = DDAHSiteMiddleware()

        middleware.process_request(request)
        self.assertEquals(request.instance, self.instance)

    def test_instance_is_none_and_domain_is_set(self):
        request = self.factory.get('/')
        request.META['SERVER_NAME'] = self.the_site.domain
        request.instance = None
        # django-subdomain-instances
        # sets urlconf in the request
        request.urlconf = 'urlconf, something'
        middleware = DDAHSiteMiddleware()

        middleware.process_request(request)
        self.assertEquals(request.instance, self.instance)
        self.assertFalse(hasattr(request, 'urlconf'))

    def test_it_doesnt_break_anything(self):
        request = self.factory.get('/')
        middleware = DDAHSiteMiddleware()
        middleware.process_request(request)
        self.assertIsInstance(request, HttpRequest)

