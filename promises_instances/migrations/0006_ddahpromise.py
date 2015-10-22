# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '__latest__'),
        ('promises_instances', '0005_auto_20150518_1623'),
    ]

    operations = [
        migrations.CreateModel(
            name='DDAHPromise',
            fields=[
                ('promise_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='promises.Promise')),
                ('instance', models.ForeignKey(related_name='promises', to='promises_instances.DDAHInstance')),
            ],
            bases=('promises.promise',),
        ),
    ]
