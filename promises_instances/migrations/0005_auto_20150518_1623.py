# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises_instances', '0004_ddahcategory_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ddahcategory',
            options={'ordering': ('order',)},
        ),
    ]
