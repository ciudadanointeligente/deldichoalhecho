# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddah_web', '0004_auto_20150505_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='ddahinstanceweb',
            name='contact',
            field=models.EmailField(max_length=254, null=True),
        ),
    ]
