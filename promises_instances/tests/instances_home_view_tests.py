from django.test import TestCase
from promises_instances.models import DDAHCategory
from instances.models import Instance
from promises.models import Promise
from django.core.urlresolvers import reverse
from django.test import Client
from popolo.models import Person
from promises.queryset import PromiseSummary


class InstanceHomeView(TestCase):
    def setUp(self):
        self.person = Person.objects.create(name=u"A person")

    def test_every_instance_has_its_promises(self):
        '''Every instance has its promises and categories'''
        instance = Instance.objects.create(label='bici', title='bicicletas')
        category = DDAHCategory.objects.create(name="Education", instance=instance)
        self.assertTrue(instance.categories)
        self.assertEquals(instance.categories.count(), 1)
        self.assertEquals(instance.categories.first(), category)
    
    def test_there_is_a_url_for_every_instance(self):
        '''There is a url for every instance'''
        instance = Instance.objects.create(label='bici', title='bicicletas')
        url = reverse('instance_home', kwargs={'slug':instance.label})
        self.assertTrue(url)
    
    def test_the_instance_home_page_contains_the_instance(self):
        '''The instance home page contains the instance'''
        instance = Instance.objects.create(label='bici', title='bicicletas')
        url = reverse('instance_home', kwargs={'slug':instance.label})
        c = Client()
        response = c.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIn('instance', response.context)
        self.assertEquals(response.context['instance'], instance)
    
    def test_the_home_page_contains_the_right_categories(self):
        '''The home page also brings the right categories as well'''
        instance1 = Instance.objects.create(label='bici1', title='bicicletas1')
        category1 = DDAHCategory.objects.create(name="Education1", instance=instance1)
        
        instance2 = Instance.objects.create(label='bici2', title='bicicletas2')
        category2 = DDAHCategory.objects.create(name="Education1", instance=instance2)

        url = reverse('instance_home', kwargs={'slug':instance1.label})
        c = Client()
        response = c.get(url)
        
        self.assertIn('categories', response.context)
        self.assertIn(category1, response.context['categories'])
        self.assertNotIn(category2, response.context['categories'])

    def test_there_is_a_summary_of_the_promises(self):
        '''There is a summary of the promises'''
        instance2 = Instance.objects.create(label='bici2', title='bicicletas2')
        category2 = DDAHCategory.objects.create(name="Education1", instance=instance2)
        promise3 = Promise.objects.create(name="this is a promise",\
                                              person = self.person,
                                              category=category2
                                              )
        promise3.fulfillment.percentage = 50
        promise3.fulfillment.save()

        instance1 = Instance.objects.create(label='bici1', title='bicicletas1')
        category1 = DDAHCategory.objects.create(name="Education1", instance=instance1)
        promise = Promise.objects.create(name="this is a promise",\
                                              person = self.person,
                                              category=category1
                                              )
        promise2 = Promise.objects.create(
                                        name="this is another promise",\
                                        person = self.person,
                                        category=category1,
                    )
        promise2.fulfillment.percentage = 100
        promise2.fulfillment.save()

        url = reverse('instance_home', kwargs={'slug':instance1.label})
        c = Client()
        response = c.get(url)
        self.assertIn('summary', response.context)
        self.assertIsInstance(response.context['summary'], PromiseSummary)
        self.assertEquals(response.context['summary'].accomplished, 1)
        self.assertEquals(response.context['summary'].no_progress, 1)
        self.assertEquals(response.context['summary'].in_progress, 0)
