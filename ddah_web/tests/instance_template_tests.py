from django.test import TestCase
from ddah_web.models import DDAHTemplate, DDAHInstanceWeb
from ddah_web import read_template_as_string


class InstanceTemplateTestCase(TestCase):
    '''There is a template which contains the html to be represented using {{moustache}}'''

    def setUp(self):
        self.default_template = read_template_as_string('instance_templates/default.html')

    def test_create_a_template(self):
        template = DDAHTemplate.objects.create()
        self.assertEquals(template.content, self.default_template)

    def test_when_creating_an_instance_it_automatically_creates_a_template(self):
        instance = DDAHInstanceWeb.objects.create(label="bici", title="Bicicletas")

        self.assertTrue(instance.template)
        self.assertEquals(instance.template.content, self.default_template)
