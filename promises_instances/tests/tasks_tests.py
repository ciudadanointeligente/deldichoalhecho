# -*- coding: utf-8 -*-
from django.test import TestCase
import os
import codecs
from ddah_web.models import DDAHInstanceWeb
from promises_instances.celery import csv_loader_task
from django.conf import settings


class CSVImporterTaskTestCase(TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.csv_file = os.path.join(current_dir, 'fixtures', 'example_data.csv')
        self.instance = DDAHInstanceWeb.objects.create(label='label', title='the title')

    def test_csv_loader_task(self):
        file_ = codecs.open(self.csv_file)
        result = csv_loader_task.delay(file_, self.instance)
        self.assertTrue(self.instance.promises.all())
        self.assertTrue(self.instance.categories.all())

