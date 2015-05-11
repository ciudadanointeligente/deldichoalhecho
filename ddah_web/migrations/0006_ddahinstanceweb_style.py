# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ddah_web', '0005_ddahinstanceweb_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='ddahinstanceweb',
            name='style',
            field=picklefield.fields.PickledObjectField(default={}, editable=False),
        ),
    ]
