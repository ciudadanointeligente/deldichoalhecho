from django.test import TestCase, RequestFactory, override_settings
from ddah_web.models import DDAHInstanceWeb
from promises_instances.models import DDAHInstance
from promises.models import Promise
from django.core.urlresolvers import reverse
import markdown
from ddah_web.views import DDAHInstanceWebView, DDAHInstanceWebJSONView
from ddah_web.models import DDAHInstanceWeb
from instances.models import Instance
import json
from django.conf import settings


class DDAHInstanceWebTestCase(TestCase):
    fixtures = ['100dias.json']

    def setUp(self):
        pass

    def test_instance_attributes(self):
        ddah_instance = DDAHInstanceWeb.objects.create(label='label', title='the title', contact='feli@ciudadanoi.org')
        self.assertEquals(ddah_instance.contact, 'feli@ciudadanoi.org')

    @override_settings(BASE_HOST='thesite.com')
    def test_get_url(self):
        ddah_instance = DDAHInstanceWeb.objects.create(label='label', title='the title')
        expected_url = 'label.thesite.com'
        self.assertEquals(ddah_instance.url, expected_url)

    def test_this_is_ddah_instance_subclass(self):
        '''This is a DDAHInstance'''

        instance = DDAHInstanceWeb.objects.create(label="bici", title="Bicicletas")
        self.assertIsInstance(instance, DDAHInstance)

    def test_instance_to_bunch(self):
        instance = DDAHInstanceWeb.objects.get(id=1)
        the_bunch = instance.get_as_bunch()
        self.assertEquals(the_bunch.title, instance.title)
        home_url = reverse('instance_home') # Expected url without the base host
        expected_url = '%s.%s%s' % (instance.label, settings.BASE_HOST, home_url)
        self.assertEquals(the_bunch.url, expected_url)
        self.assertEquals(the_bunch.description, instance.description)
        self.assertEquals(the_bunch.contact, instance.contact)
        self.assertEquals(len(the_bunch.categories), instance.categories.count())

        for category in the_bunch.categories:
            the_cat_from_database = instance.categories.get(id=category.id)
            self.assertEquals(the_cat_from_database.name, category.name)
            self.assertEquals(the_cat_from_database.slug, category.slug)
            self.assertEquals(the_cat_from_database.promises.count(), len(category.promises))

            expected_summary = Promise.objects.filter(category=the_cat_from_database).summary()
            self.assertEquals(category.summary.no_progress, expected_summary.no_progress)
            self.assertEquals(category.summary.accomplished, expected_summary.accomplished)
            self.assertEquals(category.summary.in_progress, expected_summary.in_progress)
            self.assertEquals(category.summary.total, expected_summary.total)
            self.assertEquals(category.summary.total_progress, expected_summary.total_progress)
            self.assertEquals(category.summary.accomplished_percentage, expected_summary.accomplished_percentage)
            self.assertEquals(category.summary.in_progress_percentage, expected_summary.in_progress_percentage)
            self.assertEquals(category.summary.no_progress_percentage, expected_summary.no_progress_percentage)
            for promise in category.promises:
                the_promise_from_database = the_cat_from_database.promises.get(id=promise.id)
                self.assertEquals(the_promise_from_database.name, promise.name)
                self.assertEquals(markdown.markdown(the_promise_from_database.description), promise.description)
                self.assertTrue(promise.date)
                self.assertEquals(the_promise_from_database.fulfillment.percentage, promise.fulfillment.percentage)
                self.assertEquals(the_promise_from_database.fulfillment.status, promise.fulfillment.status)
                self.assertEquals(markdown.markdown(the_promise_from_database.fulfillment.description), promise.fulfillment.description)
                for verification_doc in promise.verification_documents:
                    the_verification_doc_from_database = the_promise_from_database.verification_documents.get(id=verification_doc.id)
                    self.assertEquals(the_verification_doc_from_database.url, verification_doc.url)
                    self.assertEquals(the_verification_doc_from_database.display_name, verification_doc.display_name)

                for information_source in promise.information_sources:
                    the_information_source_from_database = the_promise_from_database.information_sources.get(id=information_source.id)
                    self.assertEquals(the_information_source_from_database.url, information_source.url)
                    self.assertEquals(the_information_source_from_database.display_name, information_source.display_name)
                for milestone in promise.milestones:
                    milestone_from_db = the_promise_from_database.milestones.get(id=milestone.id)
                    self.assertEquals(markdown.markdown(milestone_from_db.description), milestone.description)
                    self.assertTrue(milestone.date)

        expected_summary = Promise.objects.filter(category__in=instance.categories.all()).summary()
        self.assertEquals(the_bunch.summary.no_progress, expected_summary.no_progress)
        self.assertEquals(the_bunch.summary.accomplished, expected_summary.accomplished)
        self.assertEquals(the_bunch.summary.in_progress, expected_summary.in_progress)
        self.assertEquals(the_bunch.summary.total, expected_summary.total)
        self.assertEquals(the_bunch.summary.total_progress, expected_summary.total_progress)
        self.assertEquals(the_bunch.summary.accomplished_percentage, expected_summary.accomplished_percentage)
        self.assertEquals(the_bunch.summary.in_progress_percentage, expected_summary.in_progress_percentage)
        self.assertEquals(the_bunch.summary.no_progress_percentage, expected_summary.no_progress_percentage)

    def test_as_json(self):
        instance = DDAHInstanceWeb.objects.get(id=1)
        self.assertTrue(instance.to_json())


class DDAHInstancesView(TestCase):
    fixtures = ['100dias.json']

    def setUp(self):
        self.ddah_instance = DDAHInstanceWeb.objects.get(id=1)
        self.instance = Instance.objects.get(id=1)
        self.factory = RequestFactory()

    def test_get_the_thing(self):
        url = reverse('instance_home')
        request = self.factory.get(url)
        request.instance = self.instance
        response = DDAHInstanceWebView.as_view()(request)
        self.assertEquals(response.status_code, 200)
        content = response.render()
        self.assertTrue(content)
        self.assertIn(self.instance.label, response.content)

    def test_get_the_data_as_json(self):
        url = reverse('data_json')
        request = self.factory.get(url)
        request.instance = self.instance
        instance_web = DDAHInstanceWeb.objects.get(id=self.instance.id)
        response = DDAHInstanceWebJSONView.as_view()(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'application/json')
        self.assertEquals(response.content, instance_web.to_json())
        the_data = json.loads(response.content)
        self.assertTrue(the_data)

