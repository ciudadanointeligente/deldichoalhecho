from django.test import TestCase
from promises_instances.models import DDAHCategory, DDAHInstance
from promises.models import Promise
from popolo.models import Person
from promises_instances.views import InstanceDetailView
from promises.queryset import PromiseSummary


class InstanceHomeView(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name=u"A person")

    def test_every_instance_has_its_promises(self):
        '''Every instance has its promises and categories'''
        instance = DDAHInstance.objects.create(label='bici', title='bicicletas')
        category = DDAHCategory.objects.create(name="Education", instance=instance)
        self.assertTrue(instance.categories)
        self.assertEquals(instance.categories.count(), 1)
        self.assertEquals(instance.categories.first(), category)

    def test_the_instance_home_page_contains_the_instance(self):
        '''The instance home page contains the instance'''
        instance = DDAHInstance.objects.create(label='bici', title='bicicletas')
        view = InstanceDetailView()
        view.object = instance

        context = view.get_context_data()
        self.assertIn('instance', context)
        self.assertEquals(context['instance'], instance)

    def test_the_home_page_contains_the_right_categories(self):
        '''The home page also brings the right categories as well'''
        instance1 = DDAHInstance.objects.create(label='bici1', title='bicicletas1')
        category1 = DDAHCategory.objects.create(name="Education1", instance=instance1)

        instance2 = DDAHInstance.objects.create(label='bici2', title='bicicletas2')
        category2 = DDAHCategory.objects.create(name="Education1", instance=instance2)

        view = InstanceDetailView()
        view.object = instance1

        context = view.get_context_data()

        self.assertIn('categories', context)
        self.assertIn(category1, context['categories'])
        self.assertNotIn(category2, context['categories'])

    def test_there_is_a_summary_of_the_promises(self):
        '''There is a summary of the promises'''
        instance2 = DDAHInstance.objects.create(label='bici2', title='bicicletas2')
        category2 = DDAHCategory.objects.create(name="Education1", instance=instance2)
        promise3 = Promise.objects.create(name="this is a promise",
                                          person=self.person,
                                          category=category2
                                          )
        promise3.fulfillment.percentage = 50
        promise3.fulfillment.save()

        instance1 = DDAHInstance.objects.create(label='bici1', title='bicicletas1')
        category1 = DDAHCategory.objects.create(name="Education1", instance=instance1)
        Promise.objects.create(name="this is a promise",
                               person=self.person,
                               category=category1
                               )
        promise2 = Promise.objects.create(name="this is another promise",
                                          person=self.person,
                                          category=category1,
                                          )
        promise2.fulfillment.percentage = 100
        promise2.fulfillment.save()

        view = InstanceDetailView()
        view.object = instance1

        context = view.get_context_data()

        self.assertIn('summary', context)
        self.assertIsInstance(context['summary'], PromiseSummary)
        self.assertEquals(context['summary'].accomplished, 1)
        self.assertEquals(context['summary'].no_progress, 1)
        self.assertEquals(context['summary'].in_progress, 0)
