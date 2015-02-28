from django.test import TestCase
from promises_instances.models import DDAHCategory
from instances.models import Instance

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
		
