# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises_instances', '0006_ddahpromise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddahcategory',
            name='instance',
            field=models.ForeignKey(related_name='categories', blank=True, to='promises_instances.DDAHInstance', null=True),
        ),
    ]
