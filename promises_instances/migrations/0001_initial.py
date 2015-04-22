# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promises', '__first__'),
        ('instances', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DDAHCategory',
            fields=[
                ('category_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='promises.Category')),
                ('instance', models.ForeignKey(related_name='categories', to='instances.Instance')),
            ],
            bases=('promises.category',),
        ),
    ]
