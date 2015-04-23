# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises_instances', '0003_auto_20150423_1836'),
    ]

    operations = [
        migrations.CreateModel(
            name='DDAHInstanceWeb',
            fields=[
                ('ddahinstance_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='promises_instances.DDAHInstance')),
            ],
            bases=('promises_instances.ddahinstance',),
        ),
    ]
