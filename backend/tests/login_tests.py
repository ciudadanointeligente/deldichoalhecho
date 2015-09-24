# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from ddah_web.models import DDAHInstanceWeb
from django.test.utils import override_settings
from django.conf import settings

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
