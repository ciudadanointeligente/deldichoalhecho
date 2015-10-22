# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ddah_web.models import DDAHInstanceWeb
from django.test.utils import override_settings
from django.conf import settings
from backend.forms import CSVUploadForm, ColorPickerForm
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



