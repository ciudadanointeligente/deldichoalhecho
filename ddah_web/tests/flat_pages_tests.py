from django.test import TestCase, RequestFactory
from ddah_web.models import DdahFlatPage, DDAHInstanceWeb
from ddah_web.views import FlatPageView, MoustacheFlatPageTemplateResponse
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse


class DDAHFlatPageTestCase(TestCase):
    def setUp(self):
        self.instance = DDAHInstanceWeb.objects.create(label='label', title='the title')
        self.site = Site.objects.get(id=1)
        self.factory = RequestFactory()

    def test_instanciate_a_ddah_flatpage(self):
        flatpage = DdahFlatPage.objects.create(url="about",
                                               title="What about it?",
                                               content="Hello this is the content as html",
                                               enable_comments=True,
                                               instance=self.instance,
                                               )
        self.assertIsInstance(flatpage, FlatPage)
        self.assertFalse(flatpage.template_name)
        self.assertFalse(flatpage.registration_required)
        self.assertFalse(flatpage.sites.all())

    def test_get_the_view(self):
        flatpage = DdahFlatPage.objects.create(url="about",
                                               title="What about it?",
                                               content="Hello this is the content as html",
                                               enable_comments=True,
                                               instance=self.instance,
                                               )
        self.assertIsInstance(flatpage, FlatPage)
        url = reverse('flat_page', kwargs={'url': flatpage.url})
        self.assertTrue(url)
        request = self.factory.get(url)
        request.instance = self.instance
        response = FlatPageView.as_view()(request, url=flatpage.url)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response, MoustacheFlatPageTemplateResponse)
        expected_data = self.instance.get_as_bunch()
        del expected_data.summary
        del expected_data.categories
        expected_data.page_title = flatpage.title
        expected_data.page_content = flatpage.content
        expected_data.enable_comments = flatpage.enable_comments
        self.assertEquals(response.get_the_data(), expected_data)
        self.assertEquals(response.get_template(), self.instance.template)
        self.assertEquals(response.get_content(), self.instance.template.flat_page_content)
