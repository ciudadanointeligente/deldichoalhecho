# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instances', '__first__'),
        ('promises_instances', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DDAHInstance',
            fields=[
                ('instance_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='instances.Instance')),
            ],
            bases=('instances.instance',),
        ),
    ]
