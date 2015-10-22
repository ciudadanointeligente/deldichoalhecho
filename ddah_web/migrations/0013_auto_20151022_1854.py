# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ddah_web', '0012_auto_20150512_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ddahtemplate',
            name='header',
            field=models.TextField(default='    <div class="header">\n      <div class="container">\n        <h3 class="title"><a href="/">{{ title }}</a></h3>\n        <ul class="nav nav-pills">\n\n          {{ #flatpages }}\n          <li><a href="{{url}}">{{title}}</a></li>\n          {{ /flatpages }}\n          <li><a href="https://docs.google.com/document/d/1VRfCD9xDzvbOfJpnjHqUdnFtFeQ1akxix_ZQxP6EyOM/edit" target="_blank">Metodolog\xeda</a></li>\n          <li class="dropdown">\n            <a class="dropdown-toggle" data-toggle="dropdown" href="#">\n              Bachelet 2014-2018 <span class="caret"></span>\n            </a>\n            <ul class="dropdown-menu">\n              <li><a class="extra" href="http://deldichoalhecho.cl/">Programa de gob. estudio (2015)</a></li>\n              <li><a class="extra" href="http://deldichoalhecho.herokuapp.com/">Cumplimiento primeros cien d\xedas (2014)</a></li>\n              <li><a class="extra" href="http://21m14.deldichoalhecho.cl/">Discurso 21 de mayo (2014)</a></li>\n            </ul>\n          </li>\n          <li class="dropdown">\n            <a class="dropdown-toggle" data-toggle="dropdown" href="#">\n              Pi\xf1era 2010-2014 <span class="caret"></span>\n            </a>\n            <ul class="dropdown-menu">\n              <li><a class="extra" href="http://anteriores.deldichoalhecho.cl/cumplimiento-pinera-2010-2014/" target="_blank">Cierre de gobierno</a></li>\n              <li><a class="extra" href="http://anteriores.deldichoalhecho.cl/cumplimiento-de-promesas-discurso-21m-2013/" target="_blank">Discurso 21 de mayo (2013)</a></li>\n              <li><a class="extra" href="http://anteriores.deldichoalhecho.cl/cumplimiento-programa-de-gobierno-en-materia-legislativa-al-2013/" target="_blank">Programa de gob. estudio (2013)</a></li>\n              <li><a class="extra" href="http://anteriores.deldichoalhecho.cl/cumplimiento-de-promesas-discurso-21m-2011/" target="_blank">Discurso 21 de mayo (2012)</a></li>\n              <li><a class="extra" href="http://anteriores.deldichoalhecho.cl/programa-de-gobierno-2012/" target="_blank">Programa de gob. estudio (2012)</a></li>\n              <li><a class="extra" href="http://21demayo.ciudadanointeligente.org" target="_blank">Discurso 21 de mayo (2011)</a></li>\n            </ul>\n          </li>\n        </ul>\n      </div>\n    </div>\n'),
        ),
    ]
