#!/usr/bin/env python
from django.core.management import call_command
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_site.settings")
call_command('test', 'promises_web', 'promises_instances', 'ddah_web', '--failfast',verbosity=1)
