# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ddah_web.models import DDAHInstanceWeb
from django.test.utils import override_settings
from django.conf import settings
from backend.forms import CSVUploadForm, ColorPickerForm, CategoryCreateForm, PromiseCreateForm, PromiseUpdateForm
from promises_instances.models import DDAHCategory
from promises.models import Promise
import codecs
import os


PASSWORD = 'feroz'
@override_settings(ROOT_URLCONF=settings.ROOT_URLCONF_HOST)
class BackendHomeTestCaseBase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="fiera", password=PASSWORD)
        self.other_user = User.objects.create_user(username="benito", password=PASSWORD)
        self.instance = DDAHInstanceWeb.objects.create(label='label', title='the title')
        self.instance2 = DDAHInstanceWeb.objects.create(label='label2', title='the title2')
        self.instance.users.add(self.user)
        self.instance2.users.add(self.other_user)

    def test_get_home(self):
        url = reverse('backend:home')
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['instances'][0], self.instance)
        self.assertEquals(len(response.context['instances']), 1)

    def test_get_instance_view(self):
        url = reverse('backend:instance', kwargs={'slug': self.instance.label})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['instance'], self.instance)
        url = reverse('backend:instance', kwargs={'slug': self.instance2.label})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 401)



@override_settings(ROOT_URLCONF=settings.ROOT_URLCONF_HOST)
class CSVUploadTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="fiera", password=PASSWORD)
        self.other_user = User.objects.create_user(username="benito", password=PASSWORD)
        self.instance = DDAHInstanceWeb.objects.create(label='label', title='the title')
        self.instance2 = DDAHInstanceWeb.objects.create(label='label2', title='the title2')
        self.instance.users.add(self.user)
        self.instance2.users.add(self.other_user)
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        self.file_ = codecs.open(os.path.join(self.current_dir,'../../promises_instances/tests', 'fixtures', 'example_data.csv'))


    def atest_form(self):
        form = CSVUploadForm(instance=self.instance)
        file_ = codecs.open(os.path.join(self.current_dir,'../../promises_instances/tests', 'fixtures', 'example_data.csv'))
        form.csv_file = file_
        self.assertTrue(form.is_valid())
        form.upload()
        self.assertTrue(self.instance.promises.all())
        self.assertTrue(self.instance.categories.all())

    def test_get_csv_upload_view(self):
        url = reverse('backend:csv_upload', kwargs={'slug': self.instance.label})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CSVUploadForm)

    def test_post_csv_upload_view(self):
        url = reverse('backend:csv_upload', kwargs={'slug': self.instance.label})
        response = self.client.post(url, {'file': self.file_})
        self.assertRedirects(response, reverse('login') + '?next=' + url)
        self.client.login(username=self.user.username, password=PASSWORD)
        file_ = codecs.open(os.path.join(self.current_dir,'../../promises_instances/tests', 'fixtures', 'example_data.csv'))
        data = {'csv_file': file_}

        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('backend:instance', kwargs={'slug': self.instance.label}))
        self.assertTrue(self.instance.promises.all())
        self.assertTrue(self.instance.categories.all())



class CategoryCreateTestCase(BackendHomeTestCaseBase):
    def setUp(self):
        super(CategoryCreateTestCase, self).setUp()
        self.data = {"name": "New Category"}

    def test_instanciate_form(self):
        form = CategoryCreateForm(data=self.data, ddah_instance=self.instance)
        self.assertTrue(form)
        self.assertTrue(form.is_valid())
        category = form.save()
        self.assertIsInstance(category, DDAHCategory)
        self.assertEquals(category.name, 'New Category')
        self.assertEquals(category.instance, self.instance)

    def test_create_view(self):
        url = reverse('backend:create_category', kwargs={'slug': self.instance.label})
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'category_create.html')
        self.assertEquals(self.instance, response.context['instance'])
        # Posting
        original_count = self.instance.categories.count()
        data = {'name': "This is a new Category"}
        response = self.client.post(url, data=data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(original_count + 1, self.instance.categories.count())
        the_created_category = self.instance.categories.last()
        self.assertEquals(the_created_category.name, data["name"])



class PromiseCreateAndUpdateTestCase(BackendHomeTestCaseBase):
    def setUp(self):
        super(PromiseCreateAndUpdateTestCase, self).setUp()
        self.category = DDAHCategory.objects.create(instance=self.instance,
                                                    name="TheCategory")
        self.data = {"name": "Promise",
                     "description": "The description",
                     "date": "11/02/2015",
                     "ponderator": 0.2,
                     "fulfillment": 45.0}

    def test_instanciate_form(self):
        form = PromiseCreateForm(data=self.data,
                                 ddah_category=self.category)
        self.assertTrue(form)
        self.assertTrue(form.is_valid())
        promise = form.save()
        self.assertIsInstance(promise, Promise)
        self.assertEquals(promise.name, self.data["name"])
        self.assertEquals(promise.description, self.data["description"])
        self.assertEquals(promise.ponderator, 0.2)
        self.assertEquals(promise.category, self.category)
        self.assertEquals(promise.fulfillment.percentage, 45)

    def test_get_view(self):
        url = reverse('backend:create_promise', kwargs={'category_id': self.category.id,
                                                        'label': self.category.instance.label})
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['category'], self.category)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIsInstance(form, PromiseCreateForm)
        self.assertTemplateUsed(response, 'promises/promise_form.html')

    def test_post_view(self):
        url = reverse('backend:create_promise', kwargs={'category_id': self.category.id,
                                                        'label': self.category.instance.label})
        self.assertFalse(self.category.promises.all())
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(url, data=self.data, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.category.promises.all())

    def test_update_form(self):
        promise = Promise.objects.create(name="Original Promise")
        promise.fulfillment.percentage = 35
        promise.fulfillment.save()
        form = PromiseUpdateForm(instance=promise)
        self.assertEquals(form.fields['fulfillment'].initial, 35)

        form = PromiseUpdateForm(instance=promise, data=self.data)
        self.assertTrue(form.is_valid())
        promise = form.save()
        self.assertEquals(promise.name, self.data["name"])
        self.assertEquals(promise.description, self.data["description"])
        self.assertEquals(promise.ponderator, self.data["ponderator"])
        self.assertEquals(promise.fulfillment.percentage, self.data["fulfillment"])

    def test_get_update_view(self):
        promise = Promise.objects.create(name="Original Promise", category=self.category)
        url = reverse('backend:update_promise', kwargs={'pk': promise.id})
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIsInstance(form, PromiseUpdateForm)
        self.assertTemplateUsed(response, 'promises/promise_update.html')

    def test_post_update_view(self):
        promise = Promise.objects.create(name="Original Promise", category=self.category)
        url = reverse('backend:update_promise', kwargs={'pk': promise.id})
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.post(url, data=self.data, follow=True)
        self.assertEquals(response.status_code, 200)
        promise = Promise.objects.get(id=promise.id)
        self.assertEquals(promise.name, self.data["name"])
        self.assertEquals(promise.description, self.data["description"])
        self.assertEquals(promise.ponderator, self.data["ponderator"])
        self.assertEquals(promise.fulfillment.percentage, self.data["fulfillment"])


class ColorPickerFormTestCase(BackendHomeTestCaseBase):
    def setUp(self):
        super(ColorPickerFormTestCase, self).setUp()
        self.data = {
            "background_color": "Fiera",
            "second_color": "Feroz",
            "read_more_color": "Inteligente"
        }

    def test_instanciate_form(self):
        form = ColorPickerForm(data=self.data, instance=self.instance)
        self.assertTrue(form)
        self.assertTrue(form.is_valid())
        form.update_colors()
        instance = form.instance
        self.assertEquals(instance.style["background_color"],self.data["background_color"])
        self.assertEquals(instance.style["second_color"],self.data["second_color"])
        self.assertEquals(instance.style["read_more_color"],self.data["read_more_color"])

    def test_instance_initial(self):
        form = ColorPickerForm(data={}, instance=self.instance)
        self.assertEquals(form.fields["background_color"].initial, self.instance.style['background_color'])
        self.assertEquals(form.fields["second_color"].initial, self.instance.style['second_color'])
        self.assertEquals(form.fields["read_more_color"].initial, self.instance.style['read_more_color'])

    def test_color_picker_view(self):
        url = reverse('backend:instance_style', kwargs={'slug': self.instance.label})
        self.client.login(username=self.user.username, password=PASSWORD)
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertIsInstance(form, ColorPickerForm)
        # posting
        response = self.client.post(url, data=self.data, follow=True)
        self.assertEquals(response.status_code, 200)
        instance = DDAHInstanceWeb.objects.get(id=self.instance.id)
        self.assertEquals(instance.style['background_color'], self.data['background_color'])
        self.assertEquals(instance.style['second_color'], self.data['second_color'])
        self.assertEquals(instance.style['read_more_color'], self.data['read_more_color'])



