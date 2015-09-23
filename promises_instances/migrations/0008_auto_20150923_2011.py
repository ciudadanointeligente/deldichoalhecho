# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises_instances', '0007_auto_20150923_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddahpromise',
            name='instance',
            field=models.ForeignKey(related_name='promises', blank=True, to='promises_instances.DDAHInstance', null=True),
        ),
    ]
