# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises_instances', '0002_ddahinstance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddahcategory',
            name='instance',
            field=models.ForeignKey(related_name='categories', to='promises_instances.DDAHInstance'),
        ),
    ]
