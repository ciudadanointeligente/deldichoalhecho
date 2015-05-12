# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flatpages', '0001_initial'),
        ('ddah_web', '0009_auto_20150512_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='DdahFlatPage',
            fields=[
                ('flatpage_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='flatpages.FlatPage')),
                ('instance', models.ForeignKey(to='ddah_web.DDAHInstanceWeb')),
            ],
            bases=('flatpages.flatpage',),
        ),
    ]
