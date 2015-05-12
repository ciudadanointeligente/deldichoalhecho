# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddah_web', '0010_ddahflatpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='ddahtemplate',
            name='flat_page_content',
            field=models.TextField(default='<!DOCTYPE html>\n<html lang="es">\n\n  {{> head }}\n\n  <body>\n\n  {{> header }}\n\n\n    <h1>{{ title }}</h1>\n\n    <br />\n    --------------------\n    {{ content }}\n    --------------------\n    <br />\n    {{# enable_comments }}\n    Disqus\n    {{/ enable_comments }}\n\n\n    <script type="text/javascript">\n    $(document).ready(function() {\n    $(\'.category-body\').expander({\n    expandText: \'<p class="text-center category-expander"><i class="fa fa-chevron-down"></i></p>\',\n    userCollapseText: \'<p class="text-center category-expander"><i class="fa fa-chevron-up"></i></p>\',\n    slicePoint: 260,\n    expandPrefix:     \'\',\n    });\n    });\n    </script>\n\n  {{> footer }}\n\n  {{> style }}\n\n    <!-- Include all compiled plugins (below), or include individual files as needed -->\n    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>\n  </body>\n</html>\n'),
        ),
    ]
