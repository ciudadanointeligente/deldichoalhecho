# -*- coding: utf-8 -*-
from django.test import TestCase
import os
import codecs
from promises_instances.models import DDAHInstance
from promises_instances.csv_loader import DDAHCSVProcessor


class CSVCommandTestCase(TestCase):
    def setUp(self):
        super(CSVCommandTestCase, self).setUp()
        current_dir = os.path.dirname(os.path.realpath(__file__))
        self.csv_file = os.path.join(current_dir, 'fixtures', 'example_data.csv')
        self.instance = DDAHInstance.objects.create(label='label', title='the title')

    def test_command_itself(self):
        file_ = codecs.open(self.csv_file)
        processor = DDAHCSVProcessor(file_, self.instance)
        processor.work()
        self.assertTrue(self.instance.promises.all())
        self.assertTrue(self.instance.categories.all())

    def atest_call_command(self):
        from django.core.management import call_command
        call_command('ddah_importer', self.csv_file, self.instance.label)
        self.assertTrue(self.instance.promises.all())
        self.assertTrue(self.instance.categories.all())
