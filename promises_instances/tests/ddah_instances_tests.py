from django.test import TestCase
from promises_instances.models import DDAHCategory, DDAHInstance, DDAHPromise
from instances.models import Instance
from popolo.models import Person
from promises.models import Promise


class DDAHInstancesTestCase(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name=u"A person")

    def test_create_instance(self):
        '''Create an instance'''
        ddah_instance = DDAHInstance.objects.create(label='label', title='the title')
        self.assertTrue(ddah_instance)
        self.assertIsInstance(ddah_instance, Instance)

    def test_an_instance_can_have_categories(self):
        ddah_instance = DDAHInstance.objects.create(label='label', title='the title')
        category = DDAHCategory.objects.create(name="Education", instance=ddah_instance)

        self.assertIn(category, ddah_instance.categories.all())

        category = DDAHCategory.objects.create(name="Education")
        self.assertIsNone(category.instance)

    def test_an_instance_can_have_promises(self):
        ddah_instance = DDAHInstance.objects.create(label='label', title='the title')
        promise = DDAHPromise.objects.create(name='promise', instance=ddah_instance)
        self.assertIsInstance(promise, Promise)
        self.assertIn(promise, ddah_instance.promises.all())
        category = DDAHCategory.objects.create(name="Education", instance=ddah_instance)
        promise = DDAHPromise.objects.create(name='promise', category=category)
        self.assertEquals(promise.instance, ddah_instance)
        promise = DDAHPromise.objects.create(name='promise')
        self.assertIsNone(promise.instance)

    def test_category_can_have_order(self):
        ddah_instance = DDAHInstance.objects.create(label='label', title='the title')
        category1 = DDAHCategory.objects.create(name="Education1", instance=ddah_instance, order=2)
        category2 = DDAHCategory.objects.create(name="Education2", instance=ddah_instance, order=1)

        all_categories = DDAHCategory.objects.all()
        self.assertEquals(all_categories[0], category2)
        self.assertEquals(all_categories[1], category1)
