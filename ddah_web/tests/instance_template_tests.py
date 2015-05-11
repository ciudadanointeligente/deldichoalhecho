from django.test import TestCase, RequestFactory
from ddah_web.models import DDAHTemplate, DDAHInstanceWeb
from ddah_web import read_template_as_string
from ddah_web.views import MoustacheTemplateResponse


class InstanceTemplateTestCase(TestCase):
    '''There is a template which contains the html to be represented using {{moustache}}'''

    def setUp(self):
        self.default_template = read_template_as_string('instance_templates/default.html')
        self.default_template_footer = read_template_as_string('instance_templates/partials/footer.html')
        self.default_template_head = read_template_as_string('instance_templates/partials/head.html')
        self.default_template_header = read_template_as_string('instance_templates/partials/header.html')
        self.default_template_style = read_template_as_string('instance_templates/partials/style.html')

    def test_create_a_template(self):
        template = DDAHTemplate.objects.create()
        self.assertEquals(template.content, self.default_template)
        self.assertEquals(template.head, self.default_template_head)
        self.assertEquals(template.header, self.default_template_header)
        self.assertEquals(template.style, self.default_template_style)
        self.assertEquals(template.footer, self.default_template_footer)

    def test_when_creating_an_instance_it_automatically_creates_a_template(self):
        instance = DDAHInstanceWeb.objects.create(label="bici", title="Bicicletas")

        self.assertTrue(instance.template)
        self.assertEquals(instance.template.content, self.default_template)
        self.assertEquals(instance.template.head, self.default_template_head)
        self.assertEquals(instance.template.header, self.default_template_header)
        self.assertEquals(instance.template.style, self.default_template_style)
        self.assertEquals(instance.template.footer, self.default_template_footer)


class MustacheTemplateResponseTestCase(TestCase):
    def setUp(self):
        self.template = DDAHTemplate.objects.create(content="content {{> head }} {{> header }} {{> style }} {{> footer }}",
                            head="head",
                            header="header",
                            style="style",
                            footer="footer")
        self.instance = DDAHInstanceWeb.objects.create(label="bici", title="Bicicletas")
        self.instance.template = self.template
        self.factory = RequestFactory()

    def test_renderes_correctly(self):
        request = self.factory.get('/')

        response = MoustacheTemplateResponse(request, 'unused.html')
        response.context_data = {
            'instance': self.instance
        }

        rendered_text = "content head header style footer"
        self.assertEquals(rendered_text, response.rendered_content)
