# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddah_web', '0002_ddahtemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='ddahtemplate',
            name='instance',
            field=models.ForeignKey(to='ddah_web.DDAHInstanceWeb', null=True),
        ),
    ]
