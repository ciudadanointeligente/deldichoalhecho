from django.core.management.base import BaseCommand
import codecs
import django
from distutils.version import StrictVersion
from promises_instances.csv_loader import DDAHCSVProcessor
from promises_instances.models import DDAHInstance


class Command(BaseCommand):
    help = 'Imports a csv file into promises'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)
        parser.add_argument('instance_label', nargs='+', type=str)

    def handle(self, *args, **options):
        if not StrictVersion(django.get_version()) < StrictVersion("1.8"):
            file_name = options['csv_file'][0]
            label = options['instance_label'][0]
        else:
            file_name = args[0]
            label = args[1]
        file_ = codecs.open(file_name)
        instance = DDAHInstance.objects.get(label=label)
        processor = DDAHCSVProcessor(file_, instance)
        processor.work()
