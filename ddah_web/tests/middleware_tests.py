from django.test import TestCase, RequestFactory
from django.contrib.sites.models import Site
from promises_instances.models import DDAHInstance
from ddah_web.models import DDAHSiteInstance, DDAHInstanceWeb


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

