from django.test import TestCase
from ddah_web.models import DDAHInstanceWeb
from promises_instances.models import DDAHInstance
from promises.models import Promise
from django.core.urlresolvers import reverse


class DDAHInstanceWebTestCase(TestCase):
    fixtures = ['100dias.json']

    def setUp(self):
        pass

    def test_this_is_ddah_instance_subclass(self):
        '''This is a DDAHInstance'''

        instance = DDAHInstanceWeb.objects.create(label="bici", title="Bicicletas")
        self.assertIsInstance(instance, DDAHInstance)

    def test_instance_to_bunch(self):
        instance = DDAHInstanceWeb.objects.get(id=1)
        the_bunch = instance.get_as_bunch()
        self.assertEquals(the_bunch.title, instance.title)
        self.assertEquals(len(the_bunch.categories), instance.categories.count())

        for category_id in the_bunch.categories:
            category = the_bunch.categories[category_id]
            the_cat_from_database = instance.categories.get(id=category.id)
            self.assertEquals(the_cat_from_database.name, category.name)
            self.assertEquals(the_cat_from_database.slug, category.slug)
            self.assertEquals(the_cat_from_database.promises.count(), len(category.promises))
            for promise_id in category.promises:
                promise = category.promises[promise_id]
                the_promise_from_database = the_cat_from_database.promises.get(id=promise.id)
                self.assertEquals(the_promise_from_database.name, promise.name)
                self.assertEquals(the_promise_from_database.description, promise.description)
                self.assertTrue(promise.date)
                self.assertEquals(the_promise_from_database.fulfillment.percentage, promise.fulfillment.percentage)
                self.assertEquals(the_promise_from_database.fulfillment.status, promise.fulfillment.status)
                self.assertEquals(the_promise_from_database.fulfillment.description, promise.fulfillment.description)
                for verification_doc_id in promise.verification_documents:
                    verification_doc = promise.verification_documents[verification_doc_id]
                    the_verification_doc_from_database = the_promise_from_database.verification_documents.get(id=verification_doc.id)
                    self.assertEquals(the_verification_doc_from_database.url, verification_doc.url)
                    self.assertEquals(the_verification_doc_from_database.display_name, verification_doc.display_name)

                for information_source_id in promise.information_sources:
                    information_source = promise.information_sources[information_source_id]
                    the_information_source_from_database = the_promise_from_database.information_sources.get(id=information_source.id)
                    self.assertEquals(the_information_source_from_database.url, information_source.url)
                    self.assertEquals(the_information_source_from_database.display_name, information_source.display_name)
                for milestone_id in promise.milestones:
                    milestone = promise.milestones[milestone_id]
                    milestone_from_db = the_promise_from_database.milestones.get(id=milestone.id)
                    self.assertEquals(milestone_from_db.description, milestone.description)
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
        self.instance = DDAHInstanceWeb.objects.get(id=1)

    def test_get_the_thing(self):
        url = reverse('instance_home', kwargs={'slug': self.instance.label})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(response.content)
