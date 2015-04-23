from django.test import TestCase
from ddah_web.models import DDAHInstanceWeb
from promises_instances.models import DDAHInstance


class DDAHInstanceWebTestCase(TestCase):
    def setUp(self):
        pass

    def test_this_is_ddah_instance_subclass(self):
        '''This is a DDAHInstance'''

        instance = DDAHInstanceWeb.objects.create(label="bici", title="Bicicletas")
        self.assertIsInstance(instance, DDAHInstance)
