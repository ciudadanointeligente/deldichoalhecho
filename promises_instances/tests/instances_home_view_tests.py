from django.test import TestCase
from promises_instances.models import DDAHCategory
from instances.models import Instance
from django.core.urlresolvers import reverse
from django.test import Client

class InstanceHomeView(TestCase):
	def setUp(self):
		pass

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

