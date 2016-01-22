from django.test import TestCase
from promises_forms.forms import CategoryCreateForm
from ddah_web.models import DDAHInstanceWeb
from promises_instances.models import DDAHCategory


class CategoryCreationTestCase(TestCase):
    def setUp(self):
        self.instance = DDAHInstanceWeb.objects.create(label='label', title='the title')

    def test_instanciate(self):
        data = {'name': 'category name'}
        form = CategoryCreateForm(instance=self.instance, data=data)
        self.assertTrue(form.is_valid())
        category = form.save()
        self.assertEquals(category.instance, self.instance)
        self.assertEquals(category.name, data['name'])
        self.assertIsInstance(category, DDAHCategory)
