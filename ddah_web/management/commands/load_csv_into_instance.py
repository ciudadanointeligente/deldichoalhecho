# coding=utf-8
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from promises_instances.models import DDAHCategory
from ddah_web.models import DDAHInstanceWeb
import codecs
import csv
from promises.models import Promise, InformationSource
from popolo.models import Person
from datetime import datetime


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('instance', type=str)
        parser.add_argument('csv_file', type=str)
        parser.add_argument('--delete-previous',
                            dest='delete',
                            default=False,
                            help='Delete previous data')
        parser.add_argument('--no-skip-first',
                            dest='dont_skip_first',
                            default=False,
                            help='Do not skip first line')

    def handle(self, *args, **options):
        User.objects.get(username=options['username'])
        instance, created_instance = DDAHInstanceWeb.objects.get_or_create(label=options['instance'])
        if options['delete']:
            instance.categories.all().delete()
        file_ = codecs.open(options['csv_file'])
        with file_ as csv_file:
            promises_reader = csv.reader(csv_file, delimiter=',')
            first_line = True
            if options['dont_skip_first']:
                first_line = False
            for promise in promises_reader:
                if first_line:
                    first_line = False
                    continue
                category_name = promise[2]
                promise_name = promise[3]
                person_name = u"Tabaré Vásquez"
                category, created_category = DDAHCategory.objects.get_or_create(name=category_name, instance=instance)
                person, created_person = Person.objects.get_or_create(name=person_name)
                promise_, created_promise = Promise.objects.get_or_create(name=promise_name, person=person, category=category)
                i, c = InformationSource.objects.get_or_create(url='http://datauy.org',
                                                               display_name=promise[0] + u" página " + promise[1],
                                                               promise=promise_,
                                                               date=datetime.now())
